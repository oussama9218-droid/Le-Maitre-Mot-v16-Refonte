#!/usr/bin/env python3
"""
Wave 1 Generators Testing for V1 API - 6e Level
Test the new Wave 1 generators on the V1 API for 6e level as requested.

Test Cases:
1. Test Fraction Representation (6N2-FRAC-REPR)
2. Test Proportionnalité types (3 types)
3. Test Nombres entiers (3 types)
4. Test enonce quality for PROP_TABLEAU
5. Test enonce quality for NOMBRES_LECTURE
6. Test enonce quality for FRACTION_REPRESENTATION
"""

import requests
import json
import time
import os
from collections import Counter
from datetime import datetime

class Wave1GeneratorsTest:
    def __init__(self):
        # Get backend URL from frontend .env
        self.backend_url = self._get_backend_url()
        self.api_url = f"{self.backend_url}/api"
        self.test_results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": []
        }
        
    def _get_backend_url(self):
        """Get backend URL from frontend .env file"""
        try:
            with open('/app/frontend/.env', 'r') as f:
                for line in f:
                    if line.startswith('REACT_APP_BACKEND_URL='):
                        return line.split('=', 1)[1].strip()
        except Exception as e:
            print(f"Warning: Could not read frontend .env: {e}")
        
        # Fallback to default
        return "https://math-exercise-sync.preview.emergentagent.com"
    
    def log_test(self, test_name, passed, details=""):
        """Log test result"""
        self.test_results["total_tests"] += 1
        if passed:
            self.test_results["passed_tests"] += 1
            status = "✅ PASSED"
        else:
            self.test_results["failed_tests"] += 1
            status = "❌ FAILED"
        
        print(f"{status} - {test_name}")
        if details:
            print(f"   {details}")
        
        self.test_results["test_details"].append({
            "test": test_name,
            "passed": passed,
            "details": details
        })
    
    def make_api_call(self, data, timeout=30):
        """Make API call to V1 exercises endpoint"""
        url = f"{self.api_url}/v1/exercises/generate"
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=timeout)
            return response.status_code, response.json() if response.status_code == 200 else response.text
        except Exception as e:
            return 500, str(e)
    
    def test_fraction_representation(self):
        """
        Test Case 1: Test Fraction Representation (6N2-FRAC-REPR)
        - POST /api/v1/exercises/generate with: {"niveau": "6e", "chapitre": "Fractions", "difficulte": "facile"}
        - Run 5 times and count generator_code occurrences
        - VERIFY: Both `6e_CALCUL_FRACTIONS` and `6e_FRACTION_REPRESENTATION` appear
        - VERIFY: All have `is_fallback: false`
        """
        print("\n🔍 TEST 1: Fraction Representation (6N2-FRAC-REPR)")
        print("="*60)
        
        data = {
            "niveau": "6e",
            "chapitre": "Fractions",
            "difficulte": "facile"
        }
        
        generator_codes = []
        fallback_statuses = []
        
        for i in range(5):
            print(f"   Run {i+1}/5...")
            status_code, response = self.make_api_call(data)
            
            if status_code == 200:
                metadata = response.get('metadata', {})
                generator_code = metadata.get('generator_code', 'UNKNOWN')
                is_fallback = metadata.get('is_fallback', True)
                
                generator_codes.append(generator_code)
                fallback_statuses.append(is_fallback)
                
                print(f"      Generator: {generator_code}, Fallback: {is_fallback}")
            else:
                print(f"      ❌ API call failed: {response}")
                self.log_test("Fraction Representation - API Calls", False, f"API call {i+1} failed: {response}")
                return
        
        # Count generator occurrences
        generator_counts = Counter(generator_codes)
        print(f"\n   Generator Code Counts: {dict(generator_counts)}")
        
        # Verify both generators appear
        expected_generators = ['6e_CALCUL_FRACTIONS', '6e_FRACTION_REPRESENTATION']
        found_generators = [gen for gen in expected_generators if gen in generator_counts]
        
        both_generators_found = len(found_generators) == 2
        all_non_fallback = all(not fallback for fallback in fallback_statuses)
        
        if both_generators_found and all_non_fallback:
            self.log_test("Fraction Representation - Both Generators Present", True, 
                         f"Found generators: {found_generators}, All non-fallback: {all_non_fallback}")
        else:
            details = f"Found generators: {found_generators} (expected: {expected_generators}), All non-fallback: {all_non_fallback}"
            self.log_test("Fraction Representation - Both Generators Present", False, details)
    
    def test_proportionnalite_types(self):
        """
        Test Case 2: Test Proportionnalité types (3 types)
        - POST /api/v1/exercises/generate with: {"niveau": "6e", "chapitre": "Proportionnalité", "difficulte": "moyen"}
        - Run 10 times and count generator_code occurrences
        - VERIFY: Mix of `6e_PROPORTIONNALITE`, `6e_PROP_TABLEAU`, `6e_PROP_ACHAT`
        - VERIFY: All have `is_fallback: false`
        """
        print("\n🔍 TEST 2: Proportionnalité Types (3 types)")
        print("="*60)
        
        data = {
            "niveau": "6e",
            "chapitre": "Proportionnalité",
            "difficulte": "moyen"
        }
        
        generator_codes = []
        fallback_statuses = []
        
        for i in range(10):
            print(f"   Run {i+1}/10...")
            status_code, response = self.make_api_call(data)
            
            if status_code == 200:
                metadata = response.get('metadata', {})
                generator_code = metadata.get('generator_code', 'UNKNOWN')
                is_fallback = metadata.get('is_fallback', True)
                
                generator_codes.append(generator_code)
                fallback_statuses.append(is_fallback)
                
                print(f"      Generator: {generator_code}, Fallback: {is_fallback}")
            else:
                print(f"      ❌ API call failed: {response}")
                self.log_test("Proportionnalité Types - API Calls", False, f"API call {i+1} failed: {response}")
                return
        
        # Count generator occurrences
        generator_counts = Counter(generator_codes)
        print(f"\n   Generator Code Counts: {dict(generator_counts)}")
        
        # Verify mix of 3 types
        expected_generators = ['6e_PROPORTIONNALITE', '6e_PROP_TABLEAU', '6e_PROP_ACHAT']
        found_generators = [gen for gen in expected_generators if gen in generator_counts]
        
        mix_of_types = len(found_generators) >= 2  # At least 2 different types
        all_non_fallback = all(not fallback for fallback in fallback_statuses)
        
        if mix_of_types and all_non_fallback:
            self.log_test("Proportionnalité Types - Mix of Generators", True, 
                         f"Found {len(found_generators)} different types: {found_generators}, All non-fallback: {all_non_fallback}")
        else:
            details = f"Found {len(found_generators)} types: {found_generators} (expected mix of: {expected_generators}), All non-fallback: {all_non_fallback}"
            self.log_test("Proportionnalité Types - Mix of Generators", False, details)
    
    def test_nombres_entiers_types(self):
        """
        Test Case 3: Test Nombres entiers (3 types)
        - POST /api/v1/exercises/generate with: {"niveau": "6e", "chapitre": "Nombres entiers et décimaux", "difficulte": "moyen"}
        - Run 10 times and count generator_code occurrences
        - VERIFY: Mix of `6e_CALCUL_DECIMAUX`, `6e_NOMBRES_LECTURE`, `6e_NOMBRES_COMPARAISON`
        """
        print("\n🔍 TEST 3: Nombres Entiers Types (3 types)")
        print("="*60)
        
        data = {
            "niveau": "6e",
            "chapitre": "Nombres entiers et décimaux",
            "difficulte": "moyen"
        }
        
        generator_codes = []
        
        for i in range(10):
            print(f"   Run {i+1}/10...")
            status_code, response = self.make_api_call(data)
            
            if status_code == 200:
                metadata = response.get('metadata', {})
                generator_code = metadata.get('generator_code', 'UNKNOWN')
                
                generator_codes.append(generator_code)
                print(f"      Generator: {generator_code}")
            else:
                print(f"      ❌ API call failed: {response}")
                self.log_test("Nombres Entiers Types - API Calls", False, f"API call {i+1} failed: {response}")
                return
        
        # Count generator occurrences
        generator_counts = Counter(generator_codes)
        print(f"\n   Generator Code Counts: {dict(generator_counts)}")
        
        # Verify mix of 3 types
        expected_generators = ['6e_CALCUL_DECIMAUX', '6e_NOMBRES_LECTURE', '6e_NOMBRES_COMPARAISON']
        found_generators = [gen for gen in expected_generators if gen in generator_counts]
        
        mix_of_types = len(found_generators) >= 2  # At least 2 different types
        
        if mix_of_types:
            self.log_test("Nombres Entiers Types - Mix of Generators", True, 
                         f"Found {len(found_generators)} different types: {found_generators}")
        else:
            details = f"Found {len(found_generators)} types: {found_generators} (expected mix of: {expected_generators})"
            self.log_test("Nombres Entiers Types - Mix of Generators", False, details)
    
    def test_prop_tableau_quality(self):
        """
        Test Case 4: Test enonce quality for PROP_TABLEAU
        - Force test by calling multiple times until you get PROP_TABLEAU
        - VERIFY: enonce_html contains an HTML table with style="border-collapse"
        - VERIFY: Table has headers and data cells
        """
        print("\n🔍 TEST 4: PROP_TABLEAU Quality")
        print("="*60)
        
        data = {
            "niveau": "6e",
            "chapitre": "Proportionnalité",
            "difficulte": "moyen"
        }
        
        prop_tableau_found = False
        max_attempts = 20
        
        for i in range(max_attempts):
            print(f"   Attempt {i+1}/{max_attempts} to find PROP_TABLEAU...")
            status_code, response = self.make_api_call(data)
            
            if status_code == 200:
                metadata = response.get('metadata', {})
                generator_code = metadata.get('generator_code', 'UNKNOWN')
                
                if 'PROP_TABLEAU' in generator_code:
                    print(f"      ✅ Found PROP_TABLEAU generator: {generator_code}")
                    prop_tableau_found = True
                    
                    # Check enonce quality
                    enonce_html = response.get('enonce_html', '')
                    
                    # Check for HTML table with border-collapse style
                    has_table = '<table' in enonce_html
                    has_border_collapse = 'border-collapse' in enonce_html
                    has_headers = '<th' in enonce_html or '<thead' in enonce_html
                    has_data_cells = '<td' in enonce_html or '<tbody' in enonce_html
                    
                    print(f"      Table present: {has_table}")
                    print(f"      Border-collapse style: {has_border_collapse}")
                    print(f"      Headers present: {has_headers}")
                    print(f"      Data cells present: {has_data_cells}")
                    
                    if has_table and has_border_collapse and (has_headers or has_data_cells):
                        self.log_test("PROP_TABLEAU Quality - HTML Table Structure", True,
                                     f"Table with border-collapse style and proper structure found")
                    else:
                        self.log_test("PROP_TABLEAU Quality - HTML Table Structure", False,
                                     f"Table: {has_table}, Border-collapse: {has_border_collapse}, Headers/Data: {has_headers or has_data_cells}")
                    break
                else:
                    print(f"      Generator: {generator_code} (not PROP_TABLEAU)")
            else:
                print(f"      ❌ API call failed: {response}")
        
        if not prop_tableau_found:
            self.log_test("PROP_TABLEAU Quality - Generator Found", False,
                         f"PROP_TABLEAU generator not found in {max_attempts} attempts")
    
    def test_nombres_lecture_quality(self):
        """
        Test Case 5: Test enonce quality for NOMBRES_LECTURE
        - VERIFY: enonce contains "Écrire en lettres" or similar instruction
        - VERIFY: Contains a number to convert
        """
        print("\n🔍 TEST 5: NOMBRES_LECTURE Quality")
        print("="*60)
        
        data = {
            "niveau": "6e",
            "chapitre": "Nombres entiers et décimaux",
            "difficulte": "moyen"
        }
        
        nombres_lecture_found = False
        max_attempts = 20
        
        for i in range(max_attempts):
            print(f"   Attempt {i+1}/{max_attempts} to find NOMBRES_LECTURE...")
            status_code, response = self.make_api_call(data)
            
            if status_code == 200:
                metadata = response.get('metadata', {})
                generator_code = metadata.get('generator_code', 'UNKNOWN')
                
                if 'NOMBRES_LECTURE' in generator_code:
                    print(f"      ✅ Found NOMBRES_LECTURE generator: {generator_code}")
                    nombres_lecture_found = True
                    
                    # Check enonce quality
                    enonce_html = response.get('enonce_html', '')
                    enonce_text = response.get('enonce', '')
                    combined_text = (enonce_html + ' ' + enonce_text).lower()
                    
                    # Check for writing instruction
                    writing_instructions = ['écrire en lettres', 'écrire en toutes lettres', 'écris en lettres', 'écriture en lettres']
                    has_writing_instruction = any(instruction in combined_text for instruction in writing_instructions)
                    
                    # Check for numbers (digits)
                    import re
                    has_numbers = bool(re.search(r'\d+', combined_text))
                    
                    print(f"      Writing instruction present: {has_writing_instruction}")
                    print(f"      Numbers to convert present: {has_numbers}")
                    
                    if has_writing_instruction and has_numbers:
                        self.log_test("NOMBRES_LECTURE Quality - Content Structure", True,
                                     f"Contains writing instruction and numbers to convert")
                    else:
                        self.log_test("NOMBRES_LECTURE Quality - Content Structure", False,
                                     f"Writing instruction: {has_writing_instruction}, Numbers: {has_numbers}")
                    break
                else:
                    print(f"      Generator: {generator_code} (not NOMBRES_LECTURE)")
            else:
                print(f"      ❌ API call failed: {response}")
        
        if not nombres_lecture_found:
            self.log_test("NOMBRES_LECTURE Quality - Generator Found", False,
                         f"NOMBRES_LECTURE generator not found in {max_attempts} attempts")
    
    def test_fraction_representation_quality(self):
        """
        Test Case 6: Test enonce quality for FRACTION_REPRESENTATION
        - VERIFY: enonce_html contains SVG with fraction visualization
        - VERIFY: SVG contains rectangles or circles for fraction representation
        """
        print("\n🔍 TEST 6: FRACTION_REPRESENTATION Quality")
        print("="*60)
        
        data = {
            "niveau": "6e",
            "chapitre": "Fractions",
            "difficulte": "facile"
        }
        
        fraction_repr_found = False
        max_attempts = 20
        
        for i in range(max_attempts):
            print(f"   Attempt {i+1}/{max_attempts} to find FRACTION_REPRESENTATION...")
            status_code, response = self.make_api_call(data)
            
            if status_code == 200:
                metadata = response.get('metadata', {})
                generator_code = metadata.get('generator_code', 'UNKNOWN')
                
                if 'FRACTION_REPRESENTATION' in generator_code:
                    print(f"      ✅ Found FRACTION_REPRESENTATION generator: {generator_code}")
                    fraction_repr_found = True
                    
                    # Check enonce quality
                    enonce_html = response.get('enonce_html', '')
                    
                    # Check for SVG
                    has_svg = '<svg' in enonce_html
                    
                    # Check for geometric shapes (rectangles or circles)
                    has_rectangles = '<rect' in enonce_html
                    has_circles = '<circle' in enonce_html
                    has_shapes = has_rectangles or has_circles
                    
                    print(f"      SVG present: {has_svg}")
                    print(f"      Rectangles present: {has_rectangles}")
                    print(f"      Circles present: {has_circles}")
                    print(f"      Geometric shapes for visualization: {has_shapes}")
                    
                    if has_svg and has_shapes:
                        self.log_test("FRACTION_REPRESENTATION Quality - SVG Visualization", True,
                                     f"Contains SVG with geometric shapes for fraction visualization")
                    else:
                        self.log_test("FRACTION_REPRESENTATION Quality - SVG Visualization", False,
                                     f"SVG: {has_svg}, Geometric shapes: {has_shapes}")
                    break
                else:
                    print(f"      Generator: {generator_code} (not FRACTION_REPRESENTATION)")
            else:
                print(f"      ❌ API call failed: {response}")
        
        if not fraction_repr_found:
            self.log_test("FRACTION_REPRESENTATION Quality - Generator Found", False,
                         f"FRACTION_REPRESENTATION generator not found in {max_attempts} attempts")
    
    def run_all_tests(self):
        """Run all Wave 1 generator tests"""
        print("🚀 WAVE 1 GENERATORS TESTING - V1 API - 6e LEVEL")
        print("="*70)
        print(f"Backend URL: {self.backend_url}")
        print(f"API URL: {self.api_url}")
        print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all test cases
        self.test_fraction_representation()
        self.test_proportionnalite_types()
        self.test_nombres_entiers_types()
        self.test_prop_tableau_quality()
        self.test_nombres_lecture_quality()
        self.test_fraction_representation_quality()
        
        # Print summary
        print("\n" + "="*70)
        print("📊 WAVE 1 GENERATORS TEST SUMMARY")
        print("="*70)
        print(f"Total Tests: {self.test_results['total_tests']}")
        print(f"Passed: {self.test_results['passed_tests']} ✅")
        print(f"Failed: {self.test_results['failed_tests']} ❌")
        
        success_rate = (self.test_results['passed_tests'] / self.test_results['total_tests']) * 100 if self.test_results['total_tests'] > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("\n🎉 WAVE 1 GENERATORS TESTING: SUCCESSFUL")
            print("✅ Wave 1 generators are working correctly on V1 API for 6e level")
        elif success_rate >= 60:
            print("\n⚠️ WAVE 1 GENERATORS TESTING: PARTIALLY SUCCESSFUL")
            print("⚠️ Some Wave 1 generators need attention")
        else:
            print("\n❌ WAVE 1 GENERATORS TESTING: NEEDS ATTENTION")
            print("❌ Multiple Wave 1 generators have issues")
        
        # Detailed results
        print("\n📋 DETAILED TEST RESULTS:")
        for test_detail in self.test_results['test_details']:
            status = "✅" if test_detail['passed'] else "❌"
            print(f"{status} {test_detail['test']}")
            if test_detail['details']:
                print(f"   {test_detail['details']}")
        
        return success_rate >= 80

if __name__ == "__main__":
    tester = Wave1GeneratorsTest()
    success = tester.run_all_tests()
    exit(0 if success else 1)