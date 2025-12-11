#!/usr/bin/env python3
"""
Test complet de cohérence géométrique après correction du bug geometric_schema
Basé sur la review request spécifique
"""

import requests
import json
import sys
from datetime import datetime

class ComprehensiveGeometricTester:
    def __init__(self):
        self.base_url = "https://mathexercise-hub.preview.emergentagent.com"
        self.api_url = f"{self.base_url}/api"
        self.results = {
            "cercles": {"total": 0, "coherent": 0, "issues": []},
            "rectangles": {"total": 0, "coherent": 0, "issues": []},
            "trigonometrie": {"total": 0, "coherent": 0, "issues": []},
            "pythagore": {"total": 0, "coherent": 0, "issues": []},
            "triangles": {"total": 0, "coherent": 0, "issues": []},
            "thales": {"total": 0, "coherent": 0, "issues": []}
        }
        
    def test_scenario(self, name, test_data, expected_coherence_rate=80):
        """Test a specific geometric scenario"""
        print(f"\n🔍 Testing: {name}")
        print(f"   Data: {test_data['niveau']} - {test_data['chapitre']} - {test_data['nb_exercices']} exercises")
        
        try:
            response = requests.post(f"{self.api_url}/generate", json=test_data, timeout=90)
            
            if response.status_code == 200:
                data = response.json()
                exercises = data.get('document', {}).get('exercises', [])
                
                print(f"   ✅ Generated {len(exercises)} exercises")
                
                coherent_count = 0
                issues = []
                
                for i, exercise in enumerate(exercises):
                    exercise_num = i + 1
                    coherence_result = self.analyze_exercise_coherence(exercise, name.lower())
                    
                    if coherence_result["is_coherent"]:
                        coherent_count += 1
                        print(f"   ✅ Exercise {exercise_num}: COHERENT")
                    else:
                        print(f"   ❌ Exercise {exercise_num}: ISSUES")
                        for issue in coherence_result["issues"]:
                            print(f"      - {issue}")
                            issues.append(f"Ex{exercise_num}: {issue}")
                
                # Calculate coherence rate
                coherence_rate = (coherent_count / len(exercises) * 100) if exercises else 0
                
                # Store results
                category = self.get_category_from_name(name)
                if category in self.results:
                    self.results[category]["total"] = len(exercises)
                    self.results[category]["coherent"] = coherent_count
                    self.results[category]["issues"] = issues
                
                print(f"   📊 Coherence: {coherent_count}/{len(exercises)} ({coherence_rate:.1f}%)")
                
                # Determine success
                success = coherence_rate >= expected_coherence_rate
                status = "✅ PASSED" if success else "❌ FAILED"
                print(f"   {status} (Expected: ≥{expected_coherence_rate}%)")
                
                return success, coherence_rate, issues
                
            else:
                print(f"   ❌ Generation failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return False, 0, [f"Generation failed: {response.status_code}"]
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            return False, 0, [f"Exception: {e}"]
    
    def get_category_from_name(self, name):
        """Map test name to category"""
        name_lower = name.lower()
        if "cercle" in name_lower:
            return "cercles"
        elif "rectangle" in name_lower:
            return "rectangles"
        elif "trigono" in name_lower:
            return "trigonometrie"
        elif "pythagore" in name_lower:
            return "pythagore"
        elif "triangle" in name_lower:
            return "triangles"
        elif "thales" in name_lower:
            return "thales"
        return "other"
    
    def analyze_exercise_coherence(self, exercise, category):
        """Analyze exercise coherence based on category"""
        issues = []
        is_coherent = True
        
        enonce = exercise.get('enonce', '')
        spec_math = exercise.get('spec_mathematique', {})
        figure_geo = spec_math.get('figure_geometrique', {}) if spec_math else {}
        geo_schema = exercise.get('geometric_schema', {})
        
        # Basic checks
        if not enonce or len(enonce.strip()) <= 10:
            issues.append("Énoncé vide ou trop court")
            is_coherent = False
            
        if not exercise.get('figure_svg'):
            issues.append("Figure SVG manquante")
            is_coherent = False
        
        # Category-specific checks
        if "cercle" in category:
            # Check for circle-specific coherence
            if not any(term in enonce.lower() for term in ['cercle', 'rayon', 'diamètre']):
                issues.append("Termes cercle manquants dans énoncé")
                is_coherent = False
            
            # Check rayon in spec_mathematique
            longueurs_connues = figure_geo.get('longueurs_connues', {})
            if 'rayon' not in longueurs_connues:
                issues.append("Rayon non défini dans spec_mathematique.figure_geometrique.longueurs_connues")
                is_coherent = False
            
            # Check geometric_schema segments for correct rayon format
            segments = geo_schema.get('segments', [])
            rayon_correct = False
            rayon_broken = False
            
            for segment in segments:
                if isinstance(segment, list) and len(segment) >= 2:
                    if segment[0] == 'rayon':
                        rayon_correct = True
                    elif segment[0] == 'ra' and len(segment) > 2 and segment[1] == 'yon':
                        rayon_broken = True
                        issues.append("Bug geometric_schema: rayon divisé en 'ra' et 'yon'")
                        is_coherent = False
            
            if not rayon_correct and not rayon_broken:
                issues.append("Segment rayon manquant dans geometric_schema")
                is_coherent = False
        
        elif "rectangle" in category:
            # Check rectangle points
            points = figure_geo.get('points', [])
            if len(points) != 4:
                issues.append(f"Rectangle: {len(points)} points au lieu de 4")
                is_coherent = False
            
            # Check rectangle terms
            if not any(term in enonce.lower() for term in ['rectangle', 'carré', 'longueur', 'largeur']):
                issues.append("Termes rectangle manquants")
                is_coherent = False
        
        elif "trigono" in category:
            # Check for phantom points
            import re
            enonce_points = set(re.findall(r'\b[A-Z]\b', enonce))
            figure_points = set(figure_geo.get('points', []))
            phantom_points = enonce_points - figure_points
            
            if phantom_points:
                issues.append(f"Points fantômes: {sorted(phantom_points)}")
                is_coherent = False
        
        return {
            "is_coherent": is_coherent,
            "issues": issues
        }
    
    def run_comprehensive_test(self):
        """Run comprehensive geometric coherence test as per review request"""
        print("🎯 RE-TEST COMPLET DE LA COHÉRENCE GÉOMÉTRIQUE")
        print("="*70)
        print("CONTEXTE: Un bug critique a été identifié et corrigé dans geometric_schema")
        print("BUG FIXÉ: Le code divisait 'rayon' en 'ra' et 'yon' pour les cercles")
        print("OBJECTIF: Vérifier que les taux de cohérence atteignent >85%")
        
        # Test scenarios as specified in review request
        test_scenarios = [
            {
                "name": "Aires - Cercles (6e)",
                "data": {
                    "matiere": "Mathématiques",
                    "niveau": "6e",
                    "chapitre": "Aires",
                    "type_doc": "exercices",
                    "difficulte": "facile",
                    "nb_exercices": 5,
                    "versions": ["A"],
                    "guest_id": f"test_cercles_{datetime.now().strftime('%H%M%S')}"
                },
                "expected_coherence": 80,
                "focus": "Vérifier que rayon existe dans spec_mathematique et geometric_schema"
            },
            {
                "name": "Aires et périmètres - Rectangles (5e)",
                "data": {
                    "matiere": "Mathématiques",
                    "niveau": "5e",
                    "chapitre": "Aires et périmètres",
                    "type_doc": "exercices",
                    "difficulte": "facile",
                    "nb_exercices": 5,
                    "versions": ["A"],
                    "guest_id": f"test_rectangles_{datetime.now().strftime('%H%M%S')}"
                },
                "expected_coherence": 80,
                "focus": "Vérifier que 4 points sont présents"
            },
            {
                "name": "Trigonométrie (3e)",
                "data": {
                    "matiere": "Mathématiques",
                    "niveau": "3e",
                    "chapitre": "Trigonométrie",
                    "type_doc": "exercices",
                    "difficulte": "moyen",
                    "nb_exercices": 3,
                    "versions": ["A"],
                    "guest_id": f"test_trigono_{datetime.now().strftime('%H%M%S')}"
                },
                "expected_coherence": 67,  # Allow for 1 phantom point as mentioned
                "focus": "Identifier le point fantôme 'L'"
            },
            {
                "name": "Théorème de Pythagore (4e)",
                "data": {
                    "matiere": "Mathématiques",
                    "niveau": "4e",
                    "chapitre": "Théorème de Pythagore",
                    "type_doc": "exercices",
                    "difficulte": "moyen",
                    "nb_exercices": 2,
                    "versions": ["A"],
                    "guest_id": f"test_pythagore_{datetime.now().strftime('%H%M%S')}"
                },
                "expected_coherence": 100,
                "focus": "Test de non-régression"
            },
            {
                "name": "Triangles quelconques (5e)",
                "data": {
                    "matiere": "Mathématiques",
                    "niveau": "5e",
                    "chapitre": "Triangles",
                    "type_doc": "exercices",
                    "difficulte": "facile",
                    "nb_exercices": 2,
                    "versions": ["A"],
                    "guest_id": f"test_triangles_{datetime.now().strftime('%H%M%S')}"
                },
                "expected_coherence": 100,
                "focus": "Test de non-régression"
            },
            {
                "name": "Théorème de Thalès (3e)",
                "data": {
                    "matiere": "Mathématiques",
                    "niveau": "3e",
                    "chapitre": "Théorème de Thalès",
                    "type_doc": "exercices",
                    "difficulte": "moyen",
                    "nb_exercices": 2,
                    "versions": ["A"],
                    "guest_id": f"test_thales_{datetime.now().strftime('%H%M%S')}"
                },
                "expected_coherence": 100,
                "focus": "Test de non-régression"
            }
        ]
        
        # Run all tests
        passed_tests = 0
        total_tests = len(test_scenarios)
        all_issues = []
        
        for scenario in test_scenarios:
            print(f"\n{'='*60}")
            print(f"FOCUS: {scenario['focus']}")
            
            success, coherence_rate, issues = self.test_scenario(
                scenario['name'], 
                scenario['data'], 
                scenario['expected_coherence']
            )
            
            if success:
                passed_tests += 1
            
            all_issues.extend(issues)
        
        # Calculate global coherence rate
        total_exercises = sum(cat["total"] for cat in self.results.values())
        total_coherent = sum(cat["coherent"] for cat in self.results.values())
        global_coherence_rate = (total_coherent / total_exercises * 100) if total_exercises > 0 else 0
        
        # Print comprehensive summary
        print(f"\n🎯 RÉSUMÉ COMPLET DE LA COHÉRENCE GÉOMÉTRIQUE")
        print(f"="*70)
        
        print(f"\n📊 STATISTIQUES GLOBALES:")
        print(f"   Tests réussis: {passed_tests}/{total_tests}")
        print(f"   Exercices testés: {total_exercises}")
        print(f"   Exercices cohérents: {total_coherent}")
        print(f"   Taux de cohérence global: {global_coherence_rate:.1f}%")
        
        print(f"\n📋 RÉSULTATS PAR CATÉGORIE:")
        for category, results in self.results.items():
            if results["total"] > 0:
                rate = (results["coherent"] / results["total"] * 100)
                status = "✅" if rate >= 80 else "⚠️" if rate >= 67 else "❌"
                print(f"   {status} {category.capitalize()}: {results['coherent']}/{results['total']} ({rate:.1f}%)")
                
                if results["issues"]:
                    print(f"      Issues: {len(results['issues'])} détectées")
                    for issue in results["issues"][:2]:  # Show first 2 issues
                        print(f"        - {issue}")
                    if len(results["issues"]) > 2:
                        print(f"        ... et {len(results['issues']) - 2} autres")
        
        # Specific focus areas from review request
        print(f"\n🎯 CRITÈRES SPÉCIFIQUES DE LA REVIEW REQUEST:")
        
        # Cercles: Should pass from 0% to >80%
        cercles_rate = (self.results["cercles"]["coherent"] / self.results["cercles"]["total"] * 100) if self.results["cercles"]["total"] > 0 else 0
        cercles_success = cercles_rate > 80
        print(f"   {'✅' if cercles_success else '❌'} Aires - Cercles: {cercles_rate:.1f}% (Objectif: >80%)")
        
        # Rectangles: Should pass from 40% to >80%
        rectangles_rate = (self.results["rectangles"]["coherent"] / self.results["rectangles"]["total"] * 100) if self.results["rectangles"]["total"] > 0 else 0
        rectangles_success = rectangles_rate > 80
        print(f"   {'✅' if rectangles_success else '❌'} Aires et périmètres - Rectangles: {rectangles_rate:.1f}% (Objectif: >80%)")
        
        # Trigonométrie: Identify phantom point 'L'
        trigono_phantom_found = any("fantôme" in issue for issue in self.results["trigonometrie"]["issues"])
        print(f"   {'✅' if trigono_phantom_found else '❌'} Trigonométrie: Point fantôme 'L' {'identifié' if trigono_phantom_found else 'non détecté'}")
        
        # Global coherence rate: Should be >85%
        global_success = global_coherence_rate > 85
        print(f"   {'✅' if global_success else '❌'} Taux global de cohérence: {global_coherence_rate:.1f}% (Objectif: >85%)")
        
        # Non-regression tests
        non_regression_categories = ["pythagore", "triangles", "thales"]
        non_regression_success = all(
            (self.results[cat]["coherent"] / self.results[cat]["total"] * 100) == 100 
            if self.results[cat]["total"] > 0 else True
            for cat in non_regression_categories
        )
        print(f"   {'✅' if non_regression_success else '❌'} Tests de non-régression: {'Maintenus à 100%' if non_regression_success else 'Régression détectée'}")
        
        # Final assessment
        critical_success = cercles_success and rectangles_success and global_success and non_regression_success
        
        print(f"\n🎉 ÉVALUATION FINALE:")
        if critical_success:
            print(f"   ✅ BUG GEOMETRIC_SCHEMA COMPLÈTEMENT CORRIGÉ")
            print(f"   ✅ Cercles: Passer de 0% à {cercles_rate:.1f}% de cohérence")
            print(f"   ✅ Rectangles: Passer de 40% à {rectangles_rate:.1f}% de cohérence")
            print(f"   ✅ Taux global: {global_coherence_rate:.1f}% (>85%)")
            print(f"   ✅ Aucune régression sur les générateurs fonctionnels")
        else:
            print(f"   ⚠️  CORRECTION PARTIELLE - Améliorations significatives mais objectifs non atteints")
            print(f"   📊 Cercles: {cercles_rate:.1f}% (Objectif: >80%)")
            print(f"   📊 Rectangles: {rectangles_rate:.1f}% (Objectif: >80%)")
            print(f"   📊 Global: {global_coherence_rate:.1f}% (Objectif: >85%)")
        
        return critical_success, {
            "global_coherence_rate": global_coherence_rate,
            "cercles_rate": cercles_rate,
            "rectangles_rate": rectangles_rate,
            "passed_tests": passed_tests,
            "total_tests": total_tests,
            "results": self.results
        }

if __name__ == "__main__":
    tester = ComprehensiveGeometricTester()
    success, results = tester.run_comprehensive_test()
    sys.exit(0 if success else 1)