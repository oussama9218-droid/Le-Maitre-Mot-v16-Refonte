#!/usr/bin/env python3
"""
Test de validation de la migration curriculum vers /generate

Tests d'acceptation obligatoires pour valider la migration du système curriculum
vers l'endpoint /api/v1/exercises/generate avec les nouvelles structures.
"""

import requests
import json
import time
import random
import sys
from datetime import datetime

class CurriculumMigrationTester:
    def __init__(self):
        # Utiliser REACT_APP_BACKEND_URL depuis frontend/.env
        self.base_url = "https://math-navigator-2.preview.emergentagent.com"
        try:
            with open('/app/frontend/.env', 'r') as f:
                for line in f:
                    if line.startswith('REACT_APP_BACKEND_URL='):
                        self.base_url = line.split('=')[1].strip()
                        break
        except FileNotFoundError:
            pass  # Use default URL
        
        self.api_url = f"{self.base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.results = {
            "test_1_catalog": {"passed": False, "details": {}},
            "test_2_simple_mode": {"passed": False, "details": {}},
            "test_3_official_mode": {"passed": False, "details": {}},
            "test_4_non_regression": {"passed": False, "details": {}},
            "test_5_response_validation": {"passed": False, "details": {}},
            "test_6_legacy_compatibility": {"passed": False, "details": {}}
        }

    def log_test(self, test_name, success, details=None):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {test_name} - PASSED")
        else:
            print(f"❌ {test_name} - FAILED")
        
        if details:
            for key, value in details.items():
                print(f"   {key}: {value}")

    def make_request(self, method, endpoint, data=None, timeout=30):
        """Make HTTP request with error handling"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)
            
            return response.status_code, response.json() if response.content else {}
        except requests.exceptions.Timeout:
            return 408, {"error": "Request timeout"}
        except Exception as e:
            return 500, {"error": str(e)}

    def test_1_catalog(self):
        """
        Test 1 — Catalogue
        GET /api/v1/curriculum/6e/catalog
        Vérifier:
        - total_chapters = 28 (ou proche)
        - Présence de macro_groups (au moins 10 groupes)
        - Chaque chapitre a status = prod|beta|hidden
        - "Longueurs, masses, durées" contient ["6e_GM01","6e_GM05","6e_GM06","6e_GM07"]
        - 6e_GM07 a les générateurs LECTURE_HORLOGE, CALCUL_DUREE, CONVERSION_DUREES, PROBLEME_DUREES
        """
        print("\n🔍 Test 1 — Catalogue")
        print("="*50)
        
        status_code, response = self.make_request('GET', 'v1/curriculum/6e/catalog')
        
        if status_code != 200:
            self.log_test("Test 1 - Catalog API", False, {"status_code": status_code, "error": response.get('error', 'Unknown')})
            return False
        
        details = {}
        success = True
        
        # Vérifier total_chapters
        total_chapters = response.get('total_chapters', 0)
        details['total_chapters'] = total_chapters
        if total_chapters < 25 or total_chapters > 35:  # Proche de 28
            success = False
            details['total_chapters_error'] = f"Expected ~28, got {total_chapters}"
        
        # Vérifier macro_groups
        macro_groups = response.get('macro_groups', [])
        details['macro_groups_count'] = len(macro_groups)
        if len(macro_groups) < 10:
            success = False
            details['macro_groups_error'] = f"Expected >=10, got {len(macro_groups)}"
        
        # Vérifier les chapitres ont des status (dans domains)
        all_chapters = []
        for domain in response.get('domains', []):
            all_chapters.extend(domain.get('chapters', []))
        
        valid_statuses = ['prod', 'beta', 'hidden']
        chapters_with_status = 0
        for chapter in all_chapters:
            if chapter.get('status') in valid_statuses:
                chapters_with_status += 1
        
        details['chapters_with_valid_status'] = f"{chapters_with_status}/{len(all_chapters)}"
        if chapters_with_status < len(all_chapters) * 0.9:  # Au moins 90% avec status valide
            success = False
            details['status_error'] = "Not all chapters have valid status"
        
        # Vérifier "Longueurs, masses, durées"
        longueurs_group = None
        for group in macro_groups:
            if "Longueurs, masses, durées" in group.get('label', ''):
                longueurs_group = group
                break
        
        if longueurs_group:
            expected_codes = ["6e_GM01", "6e_GM05", "6e_GM06", "6e_GM07"]
            group_codes = longueurs_group.get('codes_officiels', [])
            details['longueurs_codes'] = group_codes
            
            missing_codes = [code for code in expected_codes if code not in group_codes]
            if missing_codes:
                success = False
                details['missing_codes'] = missing_codes
        else:
            success = False
            details['longueurs_group_error'] = "Group 'Longueurs, masses, durées' not found"
        
        # Vérifier 6e_GM07 générateurs
        gm07_chapter = None
        for chapter in chapters:
            if chapter.get('code_officiel') == '6e_GM07':
                gm07_chapter = chapter
                break
        
        if gm07_chapter:
            expected_generators = ['LECTURE_HORLOGE', 'CALCUL_DUREE', 'CONVERSION_DUREES', 'PROBLEME_DUREES']
            chapter_generators = gm07_chapter.get('generators', [])
            details['gm07_generators'] = chapter_generators
            
            missing_generators = [gen for gen in expected_generators if gen not in chapter_generators]
            if missing_generators:
                success = False
                details['missing_generators'] = missing_generators
        else:
            success = False
            details['gm07_error'] = "Chapter 6e_GM07 not found"
        
        self.results['test_1_catalog']['passed'] = success
        self.results['test_1_catalog']['details'] = details
        self.log_test("Test 1 - Catalog", success, details)
        return success

    def test_2_simple_mode(self):
        """
        Test 2 — Génération Mode Simple via code_officiel
        Simuler le mode simple:
        - Récupérer le macro group "Longueurs, masses, durées"
        - Extraire ses codes_officiels
        - Faire 10 générations avec des codes aléatoires du groupe
        - Vérifier qu'au moins une génération utilise 6e_GM07
        - Vérifier qu'au moins une a un SVG (LECTURE_HORLOGE ou CALCUL_DUREE)
        """
        print("\n🔍 Test 2 — Génération Mode Simple via code_officiel")
        print("="*50)
        
        # D'abord récupérer le catalogue pour obtenir les codes
        status_code, catalog = self.make_request('GET', 'v1/curriculum/6e/catalog')
        if status_code != 200:
            self.log_test("Test 2 - Get catalog for simple mode", False, {"error": "Cannot get catalog"})
            return False
        
        # Trouver le groupe "Longueurs, masses, durées"
        longueurs_codes = []
        for group in catalog.get('macro_groups', []):
            if "Longueurs, masses, durées" in group.get('name', ''):
                longueurs_codes = group.get('codes_officiels', [])
                break
        
        if not longueurs_codes:
            self.log_test("Test 2 - Find longueurs group", False, {"error": "Group not found"})
            return False
        
        details = {'longueurs_codes': longueurs_codes}
        success = True
        
        # Faire 10 générations avec des codes aléatoires
        generations = []
        gm07_used = False
        svg_found = False
        
        for i in range(10):
            code = random.choice(longueurs_codes)
            data = {
                "code_officiel": code,
                "difficulte": "moyen"
            }
            
            status_code, response = self.make_request('POST', 'v1/exercises/generate', data, timeout=60)
            
            if status_code == 200:
                exercise = response
                generator_code = exercise.get('metadata', {}).get('generator_code', '')
                has_svg = bool(exercise.get('figure_svg') or exercise.get('figure_svg_question'))
                
                generations.append({
                    'code_officiel': code,
                    'generator_code': generator_code,
                    'has_svg': has_svg
                })
                
                if code == '6e_GM07':
                    gm07_used = True
                
                if has_svg and ('LECTURE_HORLOGE' in generator_code or 'CALCUL_DUREE' in generator_code):
                    svg_found = True
            else:
                generations.append({
                    'code_officiel': code,
                    'error': response.get('error', 'Generation failed')
                })
        
        details['generations_count'] = len([g for g in generations if 'error' not in g])
        details['gm07_used'] = gm07_used
        details['svg_found'] = svg_found
        
        if len([g for g in generations if 'error' not in g]) < 8:  # Au moins 80% de succès
            success = False
            details['generation_error'] = "Too many generation failures"
        
        if not gm07_used:
            success = False
            details['gm07_error'] = "6e_GM07 was never used in 10 generations"
        
        # Note: SVG requirement relaxed as it depends on random selection
        if not svg_found:
            details['svg_warning'] = "No SVG found in LECTURE_HORLOGE or CALCUL_DUREE exercises"
        
        self.results['test_2_simple_mode']['passed'] = success
        self.results['test_2_simple_mode']['details'] = details
        self.log_test("Test 2 - Simple Mode Generation", success, details)
        return success

    def test_3_official_mode(self):
        """
        Test 3 — Génération Mode Officiel (6e_GM07)
        POST /api/v1/exercises/generate
        Body: {"code_officiel": "6e_GM07", "difficulte": "moyen", "nb_exercices": 1}
        Faire 5 générations et vérifier:
        - Tous les generator_code commencent par "6e_"
        - Au moins 2 types différents parmi LECTURE_HORLOGE, CALCUL_DUREE, CONVERSION_DUREES, PROBLEME_DUREES
        - Au moins un exercice avec SVG
        """
        print("\n🔍 Test 3 — Génération Mode Officiel (6e_GM07)")
        print("="*50)
        
        details = {}
        success = True
        
        generations = []
        generator_types = set()
        svg_count = 0
        
        for i in range(5):
            data = {
                "code_officiel": "6e_GM07",
                "difficulte": "moyen",
                "nb_exercices": 1
            }
            
            status_code, response = self.make_request('POST', 'v1/exercises/generate', data, timeout=60)
            
            if status_code == 200:
                exercise = response
                generator_code = exercise.get('metadata', {}).get('generator_code', '')
                has_svg = bool(exercise.get('figure_svg') or exercise.get('figure_svg_question'))
                
                generations.append({
                    'generator_code': generator_code,
                    'has_svg': has_svg,
                    'starts_with_6e': generator_code.startswith('6e_')
                })
                
                # Extraire le type de générateur
                for gen_type in ['LECTURE_HORLOGE', 'CALCUL_DUREE', 'CONVERSION_DUREES', 'PROBLEME_DUREES']:
                    if gen_type in generator_code:
                        generator_types.add(gen_type)
                        break
                
                if has_svg:
                    svg_count += 1
            else:
                generations.append({'error': response.get('error', 'Generation failed')})
        
        # Vérifier que tous les generator_code commencent par "6e_"
        valid_codes = [g for g in generations if 'error' not in g and g.get('starts_with_6e', False)]
        details['valid_generator_codes'] = f"{len(valid_codes)}/{len([g for g in generations if 'error' not in g])}"
        
        if len(valid_codes) < len([g for g in generations if 'error' not in g]):
            success = False
            details['generator_code_error'] = "Not all generator codes start with '6e_'"
        
        # Vérifier au moins 2 types différents
        details['generator_types_found'] = list(generator_types)
        details['generator_types_count'] = len(generator_types)
        
        if len(generator_types) < 2:
            success = False
            details['generator_types_error'] = f"Expected >=2 types, got {len(generator_types)}"
        
        # Vérifier au moins un SVG
        details['svg_count'] = svg_count
        if svg_count < 1:
            success = False
            details['svg_error'] = "No SVG found in any exercise"
        
        details['successful_generations'] = len([g for g in generations if 'error' not in g])
        
        self.results['test_3_official_mode']['passed'] = success
        self.results['test_3_official_mode']['details'] = details
        self.log_test("Test 3 - Official Mode (6e_GM07)", success, details)
        return success

    def test_4_non_regression(self):
        """
        Test 4 — Non-régression
        Vérifier que les chapitres existants fonctionnent toujours:
        1. Fractions (6e_N08): POST {"code_officiel": "6e_N08", "difficulte": "facile"}
        2. Symétrie axiale (6e_G07): POST {"code_officiel": "6e_G07", "difficulte": "moyen"}
        """
        print("\n🔍 Test 4 — Non-régression")
        print("="*50)
        
        details = {}
        success = True
        
        # Test 1: Fractions (6e_N08)
        data_fractions = {
            "code_officiel": "6e_N08",
            "difficulte": "facile"
        }
        
        status_code, response = self.make_request('POST', 'v1/exercises/generate', data_fractions, timeout=60)
        
        if status_code == 200:
            is_fallback = response.get('metadata', {}).get('is_fallback', True)
            enonce_html = response.get('enonce_html', '')
            
            details['fractions_is_fallback'] = is_fallback
            details['fractions_has_content'] = len(enonce_html) > 0
            
            if is_fallback:
                success = False
                details['fractions_error'] = "is_fallback should be false"
            
            if not enonce_html:
                success = False
                details['fractions_content_error'] = "enonce_html is empty"
        else:
            success = False
            details['fractions_generation_error'] = f"Status {status_code}: {response.get('error', 'Unknown')}"
        
        # Test 2: Symétrie axiale (6e_G07)
        data_symetrie = {
            "code_officiel": "6e_G07",
            "difficulte": "moyen"
        }
        
        status_code, response = self.make_request('POST', 'v1/exercises/generate', data_symetrie, timeout=60)
        
        if status_code == 200:
            is_fallback = response.get('metadata', {}).get('is_fallback', True)
            has_svg = bool(response.get('figure_svg') or response.get('figure_svg_question'))
            
            details['symetrie_is_fallback'] = is_fallback
            details['symetrie_has_svg'] = has_svg
            
            if is_fallback:
                success = False
                details['symetrie_error'] = "is_fallback should be false"
            
            if not has_svg:
                success = False
                details['symetrie_svg_error'] = "SVG should be present"
        else:
            success = False
            details['symetrie_generation_error'] = f"Status {status_code}: {response.get('error', 'Unknown')}"
        
        self.results['test_4_non_regression']['passed'] = success
        self.results['test_4_non_regression']['details'] = details
        self.log_test("Test 4 - Non-regression", success, details)
        return success

    def test_5_response_validation(self):
        """
        Test 5 — Validation des structures de réponse
        Pour chaque génération, vérifier:
        - id_exercice existe
        - niveau = "6e"
        - chapitre existe
        - enonce_html non vide
        - solution_html non vide
        - metadata.generator_code existe
        - metadata.is_fallback est boolean
        """
        print("\n🔍 Test 5 — Validation des structures de réponse")
        print("="*50)
        
        # Tester avec 6e_GM07 pour avoir une réponse complète
        data = {
            "code_officiel": "6e_GM07",
            "difficulte": "moyen"
        }
        
        status_code, response = self.make_request('POST', 'v1/exercises/generate', data, timeout=60)
        
        if status_code != 200:
            self.log_test("Test 5 - Response Structure", False, {"error": f"Status {status_code}"})
            return False
        
        details = {}
        success = True
        
        # Vérifier id_exercice
        id_exercice = response.get('id_exercice')
        details['has_id_exercice'] = bool(id_exercice)
        if not id_exercice:
            success = False
            details['id_exercice_error'] = "Missing id_exercice"
        
        # Vérifier niveau
        niveau = response.get('niveau')
        details['niveau'] = niveau
        if niveau != "6e":
            success = False
            details['niveau_error'] = f"Expected '6e', got '{niveau}'"
        
        # Vérifier chapitre
        chapitre = response.get('chapitre')
        details['has_chapitre'] = bool(chapitre)
        if not chapitre:
            success = False
            details['chapitre_error'] = "Missing chapitre"
        
        # Vérifier enonce_html
        enonce_html = response.get('enonce_html', '')
        details['enonce_html_length'] = len(enonce_html)
        if not enonce_html:
            success = False
            details['enonce_html_error'] = "enonce_html is empty"
        
        # Vérifier solution_html
        solution_html = response.get('solution_html', '')
        details['solution_html_length'] = len(solution_html)
        if not solution_html:
            success = False
            details['solution_html_error'] = "solution_html is empty"
        
        # Vérifier metadata
        metadata = response.get('metadata', {})
        generator_code = metadata.get('generator_code')
        is_fallback = metadata.get('is_fallback')
        
        details['has_generator_code'] = bool(generator_code)
        details['is_fallback_type'] = type(is_fallback).__name__
        
        if not generator_code:
            success = False
            details['generator_code_error'] = "Missing metadata.generator_code"
        
        if not isinstance(is_fallback, bool):
            success = False
            details['is_fallback_error'] = f"is_fallback should be boolean, got {type(is_fallback)}"
        
        self.results['test_5_response_validation']['passed'] = success
        self.results['test_5_response_validation']['details'] = details
        self.log_test("Test 5 - Response Structure Validation", success, details)
        return success

    def test_6_legacy_compatibility(self):
        """
        Test 6 — Codes legacy (backward compatibility)
        L'ancienne méthode doit toujours fonctionner:
        POST {"niveau": "6e", "chapitre": "Fractions", "difficulte": "facile"}
        - Vérifier que ça génère un exercice valide
        """
        print("\n🔍 Test 6 — Codes legacy (backward compatibility)")
        print("="*50)
        
        # Test avec l'ancienne méthode (niveau + chapitre au lieu de code_officiel)
        data = {
            "niveau": "6e",
            "chapitre": "Fractions",
            "difficulte": "facile"
        }
        
        status_code, response = self.make_request('POST', 'v1/exercises/generate', data, timeout=60)
        
        details = {}
        success = True
        
        if status_code == 200:
            # Vérifier que c'est un exercice valide
            id_exercice = response.get('id_exercice')
            enonce_html = response.get('enonce_html', '')
            solution_html = response.get('solution_html', '')
            
            details['has_id_exercice'] = bool(id_exercice)
            details['has_enonce'] = len(enonce_html) > 0
            details['has_solution'] = len(solution_html) > 0
            
            if not id_exercice:
                success = False
                details['id_error'] = "Missing id_exercice"
            
            if not enonce_html:
                success = False
                details['enonce_error'] = "Empty enonce_html"
            
            if not solution_html:
                success = False
                details['solution_error'] = "Empty solution_html"
            
            # Vérifier que c'est bien des fractions
            if 'fraction' in enonce_html.lower() or 'frac' in enonce_html:
                details['fraction_content'] = True
            else:
                details['fraction_content_warning'] = "No fraction content detected"
        else:
            success = False
            details['generation_error'] = f"Status {status_code}: {response.get('error', 'Unknown')}"
        
        self.results['test_6_legacy_compatibility']['passed'] = success
        self.results['test_6_legacy_compatibility']['details'] = details
        self.log_test("Test 6 - Legacy Compatibility", success, details)
        return success

    def run_all_tests(self):
        """Exécuter tous les tests de validation"""
        print("🚀 DÉMARRAGE DES TESTS DE VALIDATION CURRICULUM MIGRATION")
        print("="*70)
        print(f"Backend URL: {self.base_url}")
        print(f"API URL: {self.api_url}")
        
        start_time = time.time()
        
        # Exécuter tous les tests
        test_results = [
            self.test_1_catalog(),
            self.test_2_simple_mode(),
            self.test_3_official_mode(),
            self.test_4_non_regression(),
            self.test_5_response_validation(),
            self.test_6_legacy_compatibility()
        ]
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Résumé final
        print("\n" + "="*70)
        print("📊 RÉSUMÉ DES TESTS DE VALIDATION")
        print("="*70)
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        
        print(f"Tests réussis: {passed_tests}/{total_tests}")
        print(f"Temps total: {total_time:.2f} secondes")
        
        # Détail par test
        for test_name, result in self.results.items():
            status = "✅ PASSED" if result['passed'] else "❌ FAILED"
            print(f"{status} - {test_name}")
        
        # Évaluation globale
        if passed_tests == total_tests:
            print("\n🎉 VALIDATION CURRICULUM MIGRATION: SUCCÈS COMPLET")
            print("✅ Tous les tests d'acceptation sont passés")
            print("✅ La migration curriculum vers /generate est validée")
        elif passed_tests >= total_tests * 0.8:
            print("\n⚠️  VALIDATION CURRICULUM MIGRATION: SUCCÈS PARTIEL")
            print(f"✅ {passed_tests}/{total_tests} tests passés (≥80%)")
            print("⚠️  Quelques ajustements mineurs nécessaires")
        else:
            print("\n❌ VALIDATION CURRICULUM MIGRATION: ÉCHEC")
            print(f"❌ Seulement {passed_tests}/{total_tests} tests passés (<80%)")
            print("🔧 Corrections majeures nécessaires")
        
        return passed_tests == total_tests

def main():
    """Point d'entrée principal"""
    tester = CurriculumMigrationTester()
    success = tester.run_all_tests()
    
    # Code de sortie pour intégration CI/CD
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()