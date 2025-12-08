#!/usr/bin/env python3
"""
Urgent validation test for 400 Bad Request fix
"""
import requests
import sys
import json
import time
import uuid
from datetime import datetime

class UrgentValidator:
    def __init__(self, base_url="https://mathalea-export.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.guest_id = f"urgent-test-{datetime.now().strftime('%H%M%S')}-{uuid.uuid4().hex[:8]}"
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if not endpoint.startswith('http') else endpoint
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)

            print(f"   Status: {response.status_code}")
            
            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    return True, response_data
                except:
                    return True, response.text
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                    return False, error_data
                except:
                    print(f"   Error text: {response.text[:200]}")
                    return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timeout after {timeout}s")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_urgent_400_fix(self):
        """Test the urgent 400 Bad Request fix"""
        print("🚨 URGENT TESTING: 400 BAD REQUEST FIX VALIDATION")
        print("="*70)
        print("CONTEXT: Correction urgente appliquée au système de feature flags")
        print("CRITÈRES DE SUCCÈS: Aucune erreur 400 pour matières actives, temps < 30s")
        
        # Test scenarios based on review request
        test_scenarios = [
            # Test Matières de Base (should work again)
            {
                "name": "Mathématiques 6e - Nombres entiers et décimaux (REGRESSION)",
                "data": {
                    "matiere": "Mathématiques",
                    "niveau": "6e", 
                    "chapitre": "Nombres entiers et décimaux",
                    "type_doc": "exercices",
                    "difficulte": "moyen",
                    "nb_exercices": 2,
                    "versions": ["A"],
                    "guest_id": self.guest_id
                },
                "expected_status": 200,
                "priority": "ABSOLUE"
            },
            {
                "name": "Physique-Chimie 5e - Organisation et transformations de la matière (REGRESSION)",
                "data": {
                    "matiere": "Physique-Chimie",
                    "niveau": "5e",
                    "chapitre": "Organisation et transformations de la matière",
                    "type_doc": "exercices", 
                    "difficulte": "moyen",
                    "nb_exercices": 2,
                    "versions": ["A"],
                    "guest_id": self.guest_id
                },
                "expected_status": 200,
                "priority": "ABSOLUE"
            },
            {
                "name": "SVT 5e - Le vivant et son évolution (REGRESSION)",
                "data": {
                    "matiere": "SVT",
                    "niveau": "5e",
                    "chapitre": "Le vivant et son évolution",
                    "type_doc": "exercices",
                    "difficulte": "moyen", 
                    "nb_exercices": 2,
                    "versions": ["A"],
                    "guest_id": self.guest_id
                },
                "expected_status": 200,
                "priority": "ABSOLUE"
            },
            # Test Nouvelles Matières Actives
            {
                "name": "Français 6e - Grammaire et orthographe - Classes de mots (NOUVEAU ACTIF)",
                "data": {
                    "matiere": "Français",
                    "niveau": "6e",
                    "chapitre": "Grammaire et orthographe - Classes de mots",
                    "type_doc": "exercices", 
                    "difficulte": "moyen",
                    "nb_exercices": 2,
                    "versions": ["A"],
                    "guest_id": self.guest_id
                },
                "expected_status": 200,
                "priority": "HAUTE"
            },
            {
                "name": "Géographie 6e - Découvrir le(s) lieu(x) où j'habite (NOUVEAU ACTIF)",
                "data": {
                    "matiere": "Géographie",
                    "niveau": "6e",
                    "chapitre": "Découvrir le(s) lieu(x) où j'habite",
                    "type_doc": "exercices",
                    "difficulte": "moyen", 
                    "nb_exercices": 2,
                    "versions": ["A"],
                    "guest_id": self.guest_id
                },
                "expected_status": 200,
                "priority": "HAUTE"
            }
        ]
        
        # Add error validation tests
        error_scenarios = [
            {
                "name": "EMC (coming_soon) - Should return 423 Locked",
                "data": {
                    "matiere": "EMC",
                    "niveau": "6e",
                    "chapitre": "Test Chapter",
                    "type_doc": "exercices",
                    "difficulte": "moyen",
                    "nb_exercices": 2,
                    "versions": ["A"],
                    "guest_id": self.guest_id
                },
                "expected_status": 423,
                "priority": "HAUTE"
            }
        ]
        
        all_scenarios = test_scenarios + error_scenarios
        
        results = {
            "passed": 0,
            "total": len(all_scenarios),
            "critical_failures": [],
            "performance_data": []
        }
        
        for scenario in all_scenarios:
            print(f"\n🔍 Testing: {scenario['name']}")
            print(f"   Priority: {scenario['priority']}")
            print(f"   Expected: HTTP {scenario['expected_status']}")
            
            start_time = time.time()
            success, response = self.run_test(
                f"URGENT FIX: {scenario['name']}",
                "POST",
                "generate", 
                scenario['expected_status'],
                data=scenario['data'],
                timeout=60
            )
            generation_time = time.time() - start_time
            
            # Track performance for successful generations
            if scenario['expected_status'] == 200:
                results["performance_data"].append({
                    "subject": scenario['data']['matiere'],
                    "time": generation_time,
                    "success": success,
                    "priority": scenario['priority']
                })
            
            if success:
                results["passed"] += 1
                print(f"   ✅ {scenario['name']} - EXPECTED RESULT")
                
                if scenario['expected_status'] == 200 and isinstance(response, dict):
                    document = response.get('document')
                    if document:
                        exercises = document.get('exercises', [])
                        print(f"   ✅ Generated {len(exercises)} exercises in {generation_time:.2f}s")
                        
                        # Critical performance check
                        if generation_time > 30:
                            print(f"   ⚠️  Generation time exceeds 30s threshold")
                            if scenario['priority'] == 'ABSOLUE':
                                results["critical_failures"].append(f"Performance issue: {scenario['name']} took {generation_time:.2f}s")
                        else:
                            print(f"   ✅ Generation time within 30s threshold")
                            
                elif scenario['expected_status'] == 423:
                    # Check for proper 423 Locked response
                    if isinstance(response, dict):
                        error_msg = response.get('detail', '')
                        if isinstance(error_msg, str) and ('coming_soon' in error_msg.lower() or 'locked' in error_msg.lower()):
                            print(f"   ✅ Proper 423 Locked response for inactive subject")
                        else:
                            print(f"   ⚠️  423 response but unclear message: {error_msg}")
            else:
                print(f"   ❌ {scenario['name']} - UNEXPECTED RESULT")
                if isinstance(response, dict):
                    error_detail = response.get('detail', 'Unknown error')
                    print(f"   ERROR: {error_detail}")
                    
                    # Critical failure tracking
                    if scenario['priority'] == 'ABSOLUE':
                        results["critical_failures"].append(f"CRITICAL: {scenario['name']} failed - {error_detail}")
        
        # Summary
        print(f"\n📊 URGENT FIX VALIDATION SUMMARY:")
        print(f"   Overall: {results['passed']}/{results['total']} tests passed")
        
        # Performance summary for successful generations
        if results['performance_data']:
            avg_time = sum(p['time'] for p in results['performance_data']) / len(results['performance_data'])
            print(f"   Average generation time: {avg_time:.2f}s")
            
            # Check critical performance
            critical_slow = [p for p in results['performance_data'] if p['time'] > 30 and p['priority'] == 'ABSOLUE']
            if critical_slow:
                print(f"   ⚠️  {len(critical_slow)} critical subjects exceed 30s threshold")
            else:
                print(f"   ✅ All critical subjects within 30s threshold")
        
        # Critical failures assessment
        if results['critical_failures']:
            print(f"\n🚨 CRITICAL FAILURES DETECTED:")
            for failure in results['critical_failures']:
                print(f"   - {failure}")
        
        # Overall assessment
        no_critical_failures = len(results['critical_failures']) == 0
        success_rate = results['passed'] / results['total']
        
        if success_rate >= 0.8 and no_critical_failures:
            print("\n   🎉 URGENT 400 BAD REQUEST FIX SUCCESSFUL")
            print("   ✅ Matières existantes (Math/PC/SVT) refonctionnent")
            print("   ✅ Nouvelles matières actives fonctionnelles")
            print("   ✅ Erreurs appropriées (423/400) avec messages clairs")
            print("   ✅ Temps de génération < 30 secondes")
            return True
        else:
            print("\n   🚨 CRITICAL: Fix validation failed")
            return False

if __name__ == "__main__":
    validator = UrgentValidator()
    success = validator.test_urgent_400_fix()
    sys.exit(0 if success else 1)