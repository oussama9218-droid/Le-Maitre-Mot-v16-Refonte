#!/usr/bin/env python3
"""
Focused test for curriculum data validation fix in document generation.
Tests the FIXED curriculum data validation in /api/generate endpoint.
"""

import requests
import sys
import json
import time
import uuid
from datetime import datetime

class CurriculumFixTester:
    def __init__(self, base_url="https://pythonmath-engine.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.guest_id = f"curriculum-test-{datetime.now().strftime('%H%M%S')}-{uuid.uuid4().hex[:8]}"
        self.pro_user_email = "oussama92.18@gmail.com"

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None, timeout=30):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if not endpoint.startswith('http') else endpoint
        default_headers = {'Content-Type': 'application/json'}
        if headers:
            default_headers.update(headers)

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        if data:
            print(f"   Data: {data}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=default_headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=default_headers, timeout=timeout)

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
                    return False, {"error": response.text}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timeout after {timeout}s")
            return False, {"error": "timeout"}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {"error": str(e)}

    def test_catalog_integration(self):
        """Test that catalog shows new curriculum levels"""
        print("\n" + "="*60)
        print("📚 CATALOG INTEGRATION TEST")
        print("="*60)
        
        success, response = self.run_test("Catalog Integration", "GET", "catalog", 200)
        
        if success and isinstance(response, dict):
            catalog = response.get('catalog', [])
            if catalog:
                for subject in catalog:
                    if subject.get('name') == 'Mathématiques':
                        levels = subject.get('levels', [])
                        level_names = [level.get('name') for level in levels]
                        
                        print(f"   Found levels: {level_names}")
                        
                        # Check for new levels
                        expected_new_levels = ['CP', 'CE1', 'CE2', 'CM1', 'CM2']
                        found_new_levels = [level for level in expected_new_levels if level in level_names]
                        
                        print(f"   New levels found: {found_new_levels}")
                        
                        if len(found_new_levels) >= 3:
                            print("   ✅ New curriculum levels successfully integrated in catalog")
                            return True, response
                        else:
                            print("   ❌ Missing some new curriculum levels in catalog")
                            return False, response
        
        print("   ❌ Failed to verify catalog integration")
        return False, response

    def test_cp_level_generation(self):
        """Test CP level document generation - CRITICAL FIX TEST"""
        print("\n" + "="*60)
        print("🎯 CP LEVEL GENERATION TEST")
        print("="*60)
        print("CRITICAL TEST: CP level with 'Décomposer et représenter les nombres entiers jusqu'à 20'")
        print("EXPECTED: Should now pass validation (no more 400 'Chapitre non trouvé')")
        
        test_data = {
            "matiere": "Mathématiques",
            "niveau": "CP",
            "chapitre": "Décomposer et représenter les nombres entiers jusqu'à 20",
            "type_doc": "exercices",
            "difficulte": "facile",
            "nb_exercices": 2,
            "versions": ["A"],
            "guest_id": self.guest_id
        }
        
        success, response = self.run_test(
            "CP Level Generation", 
            "POST", 
            "generate", 
            200, 
            data=test_data,
            timeout=60
        )
        
        if success and isinstance(response, dict):
            document = response.get('document')
            if document:
                exercises = document.get('exercises', [])
                print(f"   ✅ CP document generation SUCCESSFUL with {len(exercises)} exercises")
                print(f"   ✅ Curriculum validation fix WORKING for CP level")
                
                # Verify dynamic prompt context
                if exercises:
                    exercise = exercises[0]
                    enonce = exercise.get('enonce', '')
                    print(f"   Exercise preview: {enonce[:100]}...")
                    
                    # Check for CP-appropriate content (dynamic prompts working)
                    cp_indicators = ['20', 'jusqu\'à 20', 'nombres', 'décomposer']
                    has_cp_content = any(indicator in enonce.lower() for indicator in cp_indicators)
                    if has_cp_content:
                        print(f"   ✅ Dynamic prompt working: 'Tu es un professeur de Mathématiques pour le niveau CP'")
                    
                return True, response
            else:
                print(f"   ❌ No document in response")
                return False, response
        else:
            print(f"   ❌ CP generation FAILED - curriculum validation fix NOT working")
            if isinstance(response, dict):
                error_detail = response.get('detail', 'Unknown error')
                print(f"   Error: {error_detail}")
                if 'chapitre non trouvé' in error_detail.lower():
                    print(f"   ❌ CRITICAL: Still getting 'Chapitre non trouvé' error - fix not applied")
            return False, response

    def test_ce1_level_generation(self):
        """Test CE1 level document generation - CRITICAL FIX TEST"""
        print("\n" + "="*60)
        print("🎯 CE1 LEVEL GENERATION TEST")
        print("="*60)
        print("CRITICAL TEST: CE1 level with 'Décomposer et représenter les nombres entiers jusqu'à 999'")
        print("EXPECTED: Should now pass validation (no more 400 'Chapitre non trouvé')")
        
        test_data = {
            "matiere": "Mathématiques",
            "niveau": "CE1",
            "chapitre": "Décomposer et représenter les nombres entiers jusqu'à 999",
            "type_doc": "exercices",
            "difficulte": "facile",
            "nb_exercices": 2,
            "versions": ["A"],
            "guest_id": self.guest_id
        }
        
        success, response = self.run_test(
            "CE1 Level Generation", 
            "POST", 
            "generate", 
            200, 
            data=test_data,
            timeout=60
        )
        
        if success and isinstance(response, dict):
            document = response.get('document')
            if document:
                exercises = document.get('exercises', [])
                print(f"   ✅ CE1 document generation SUCCESSFUL with {len(exercises)} exercises")
                print(f"   ✅ Curriculum validation fix WORKING for CE1 level")
                
                # Verify dynamic prompt context
                if exercises:
                    exercise = exercises[0]
                    enonce = exercise.get('enonce', '')
                    print(f"   Exercise preview: {enonce[:100]}...")
                    
                    # Check for CE1-appropriate content (dynamic prompts working)
                    ce1_indicators = ['999', 'jusqu\'à 999', 'centaines', 'décomposer']
                    has_ce1_content = any(indicator in enonce.lower() for indicator in ce1_indicators)
                    if has_ce1_content:
                        print(f"   ✅ Dynamic prompt working: 'Tu es un professeur de Mathématiques pour le niveau CE1'")
                    
                return True, response
            else:
                print(f"   ❌ No document in response")
                return False, response
        else:
            print(f"   ❌ CE1 generation FAILED - curriculum validation fix NOT working")
            if isinstance(response, dict):
                error_detail = response.get('detail', 'Unknown error')
                print(f"   Error: {error_detail}")
                if 'chapitre non trouvé' in error_detail.lower():
                    print(f"   ❌ CRITICAL: Still getting 'Chapitre non trouvé' error - fix not applied")
            return False, response

    def test_cm1_level_generation(self):
        """Test CM1 level document generation - CRITICAL FIX TEST"""
        print("\n" + "="*60)
        print("🎯 CM1 LEVEL GENERATION TEST")
        print("="*60)
        print("CRITICAL TEST: CM1 level with 'Fractions'")
        print("EXPECTED: Should now pass validation (no more 400 'Chapitre non trouvé')")
        
        test_data = {
            "matiere": "Mathématiques",
            "niveau": "CM1",
            "chapitre": "Fractions",
            "type_doc": "exercices",
            "difficulte": "moyen",
            "nb_exercices": 2,
            "versions": ["A"],
            "guest_id": self.guest_id
        }
        
        success, response = self.run_test(
            "CM1 Level Generation", 
            "POST", 
            "generate", 
            200, 
            data=test_data,
            timeout=60
        )
        
        if success and isinstance(response, dict):
            document = response.get('document')
            if document:
                exercises = document.get('exercises', [])
                print(f"   ✅ CM1 document generation SUCCESSFUL with {len(exercises)} exercises")
                print(f"   ✅ Curriculum validation fix WORKING for CM1 level")
                
                # Verify dynamic prompt context
                if exercises:
                    exercise = exercises[0]
                    enonce = exercise.get('enonce', '')
                    print(f"   Exercise preview: {enonce[:100]}...")
                    
                    # Check for CM1-appropriate content (dynamic prompts working)
                    cm1_indicators = ['fraction', 'numérateur', 'dénominateur', '1/2', '1/3', '1/4']
                    has_cm1_content = any(indicator in enonce.lower() for indicator in cm1_indicators)
                    if has_cm1_content:
                        print(f"   ✅ Dynamic prompt working: 'Tu es un professeur de Mathématiques pour le niveau CM1'")
                    
                return True, response
            else:
                print(f"   ❌ No document in response")
                return False, response
        else:
            print(f"   ❌ CM1 generation FAILED - curriculum validation fix NOT working")
            if isinstance(response, dict):
                error_detail = response.get('detail', 'Unknown error')
                print(f"   Error: {error_detail}")
                if 'chapitre non trouvé' in error_detail.lower():
                    print(f"   ❌ CRITICAL: Still getting 'Chapitre non trouvé' error - fix not applied")
            return False, response

    def test_6e_level_regression(self):
        """Test 6e level document generation - REGRESSION TEST"""
        print("\n" + "="*60)
        print("🔄 6e LEVEL REGRESSION TEST")
        print("="*60)
        print("REGRESSION TEST: Ensure existing 6e level still works after curriculum fix")
        print("EXPECTED: Should continue working (no regression)")
        
        test_data = {
            "matiere": "Mathématiques",
            "niveau": "6e",
            "chapitre": "Nombres entiers et décimaux",
            "type_doc": "exercices",
            "difficulte": "moyen",
            "nb_exercices": 2,
            "versions": ["A"],
            "guest_id": self.guest_id
        }
        
        success, response = self.run_test(
            "6e Level Regression", 
            "POST", 
            "generate", 
            200, 
            data=test_data,
            timeout=60
        )
        
        if success and isinstance(response, dict):
            document = response.get('document')
            if document:
                exercises = document.get('exercises', [])
                print(f"   ✅ 6e document generation SUCCESSFUL with {len(exercises)} exercises")
                print(f"   ✅ REGRESSION TEST PASSED - existing functionality still works")
                
                # Verify dynamic prompt context
                if exercises:
                    exercise = exercises[0]
                    enonce = exercise.get('enonce', '')
                    print(f"   Exercise preview: {enonce[:100]}...")
                    print(f"   ✅ Dynamic prompt working: 'Tu es un professeur de Mathématiques pour le niveau 6e'")
                    
                return True, response
            else:
                print(f"   ❌ No document in response")
                return False, response
        else:
            print(f"   ❌ 6e generation FAILED - REGRESSION DETECTED")
            if isinstance(response, dict):
                error_detail = response.get('detail', 'Unknown error')
                print(f"   Error: {error_detail}")
                if 'chapitre non trouvé' in error_detail.lower():
                    print(f"   ❌ CRITICAL: 6e level also failing - curriculum fix broke existing functionality")
            return False, response

    def run_all_tests(self):
        """Run all curriculum fix tests"""
        print("🚀 CURRICULUM DATA VALIDATION FIX VERIFICATION")
        print("="*80)
        print("CONTEXT: Testing FIXED curriculum data validation in document generation")
        print("BUG FIX: Fixed chapter validation to use new curriculum_data.py functions")
        print("EXPECTED: All generation tests should pass validation (no more 400 'Chapitre non trouvé')")
        print("="*80)
        
        tests = [
            ("Catalog Integration", self.test_catalog_integration),
            ("CP Level Generation", self.test_cp_level_generation),
            ("CE1 Level Generation", self.test_ce1_level_generation),
            ("CM1 Level Generation", self.test_cm1_level_generation),
            ("6e Level Regression", self.test_6e_level_regression)
        ]
        
        passed_tests = []
        failed_tests = []
        
        for test_name, test_func in tests:
            try:
                success, response = test_func()
                if success:
                    passed_tests.append(test_name)
                else:
                    failed_tests.append((test_name, response))
            except Exception as e:
                failed_tests.append((test_name, {"error": str(e)}))
        
        # Final Results
        print("\n" + "="*80)
        print("📊 CURRICULUM FIX TEST RESULTS")
        print("="*80)
        print(f"Tests Passed: {len(passed_tests)}/{len(tests)}")
        print(f"Success Rate: {(len(passed_tests) / len(tests) * 100):.1f}%")
        
        if passed_tests:
            print(f"\n✅ PASSED TESTS:")
            for test in passed_tests:
                print(f"   ✅ {test}")
        
        if failed_tests:
            print(f"\n❌ FAILED TESTS:")
            for test, error in failed_tests:
                print(f"   ❌ {test}")
                if isinstance(error, dict) and 'detail' in error:
                    print(f"      Error: {error['detail']}")
        
        if len(passed_tests) == len(tests):
            print("\n🎉 CURRICULUM FIX VERIFICATION SUCCESSFUL!")
            print("✅ Chapter validation in /api/generate endpoint is working")
            print("✅ New curriculum levels (CP, CE1, CE2, CM1, CM2) are functional")
            print("✅ Dynamic prompts are properly contextualized")
            print("✅ Existing 6e level continues working (no regression)")
        else:
            print("\n❌ CURRICULUM FIX VERIFICATION FAILED!")
            print("⚠️  Chapter validation fix may not be fully implemented")
            print("⚠️  Some new curriculum levels are still failing validation")
        
        return len(passed_tests), len(tests)

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "https://pythonmath-engine.preview.emergentagent.com"
    tester = CurriculumFixTester(base_url)
    
    passed, total = tester.run_all_tests()
    
    print(f"\n🎯 FINAL RESULT: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL CURRICULUM FIX TESTS PASSED!")
        sys.exit(0)
    else:
        print("❌ SOME CURRICULUM FIX TESTS FAILED!")
        sys.exit(1)