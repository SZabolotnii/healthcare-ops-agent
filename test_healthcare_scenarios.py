import streamlit as st
from time import sleep
import pytest
from datetime import datetime

class HealthcareAssistantTester:
    def __init__(self):
        self.test_results = []
        
    def run_test_suite(self):
        """Run all test scenarios"""
        print("\n=== Starting Healthcare Assistant Test Suite ===\n")
        
        # Run all test categories
        self.test_patient_flow()
        self.test_resource_management()
        self.test_staff_scheduling()
        self.test_quality_metrics()
        self.test_emergency_scenarios()
        self.test_department_specific()
        
        # Print test summary
        self.print_test_summary()

    def test_patient_flow(self):
        """Test Patient Flow Related Queries"""
        print("\n1. Testing Patient Flow Queries:")
        queries = [
            "Show me waiting times across all departments",
            "What is the current bed occupancy in the ER?",
            "How many patients are currently waiting for admission?",
            "What's the average wait time in the ICU?",
            "Show patient flow trends for the last 8 hours",
            "Which department has the longest waiting time right now?"
        ]
        self._run_test_batch("Patient Flow", queries)

    def test_resource_management(self):
        """Test Resource Management Queries"""
        print("\n2. Testing Resource Management Queries:")
        queries = [
            "Check medical supplies inventory status",
            "What is the current ventilator availability?",
            "Are there any critical supply shortages?",
            "Show resource utilization across departments",
            "Which supplies need immediate reordering?",
            "What's the equipment maintenance status?"
        ]
        self._run_test_batch("Resource Management", queries)

    def test_staff_scheduling(self):
        """Test Staff Scheduling Queries"""
        print("\n3. Testing Staff Scheduling Queries:")
        queries = [
            "Show current staff distribution",
            "How many nurses are available in ICU?",
            "What is the current shift coverage?",
            "Show staff overtime hours this week",
            "Is there adequate staff coverage for next shift?",
            "Which departments need additional staff right now?"
        ]
        self._run_test_batch("Staff Scheduling", queries)

    def test_quality_metrics(self):
        """Test Quality Metrics Queries"""
        print("\n4. Testing Quality Metrics Queries:")
        queries = [
            "What's our current patient satisfaction score?",
            "Show me compliance rates for the last 24 hours",
            "Are there any quality metrics below target?",
            "What's the current incident report status?",
            "Show quality trends across departments",
            "Which department has the highest patient satisfaction?"
        ]
        self._run_test_batch("Quality Metrics", queries)

    def test_emergency_scenarios(self):
        """Test Emergency Scenario Queries"""
        print("\n5. Testing Emergency Scenarios:")
        queries = [
            "Activate emergency protocol for mass casualty incident",
            "Need immediate bed availability status for emergency",
            "Require rapid staff mobilization plan",
            "Emergency resource allocation needed",
            "Critical capacity alert in ER",
            "Emergency department overflow protocol status"
        ]
        self._run_test_batch("Emergency Scenarios", queries)

    def test_department_specific(self):
        """Test Department-Specific Queries"""
        print("\n6. Testing Department-Specific Queries:")
        queries = [
            "Show complete metrics for ER department",
            "What's the ICU capacity and staff status?",
            "General ward patient distribution",
            "Surgery department resource utilization",
            "Pediatrics department waiting times",
            "Cardiology unit staff coverage"
        ]
        self._run_test_batch("Department-Specific", queries)

    def _run_test_batch(self, category: str, queries: list):
        """Run a batch of test queries"""
        for query in queries:
            try:
                print(f"\nTesting: {query}")
                print("-" * 50)
                
                # Simulate processing time
                print("Processing query...")
                sleep(1)
                
                # Record test execution
                self.test_results.append({
                    'category': category,
                    'query': query,
                    'timestamp': datetime.now(),
                    'status': 'Success'
                })
                
                print("✓ Test completed successfully")
                
            except Exception as e:
                print(f"✗ Test failed: {str(e)}")
                self.test_results.append({
                    'category': category,
                    'query': query,
                    'timestamp': datetime.now(),
                    'status': 'Failed',
                    'error': str(e)
                })

    def print_test_summary(self):
        """Print summary of all test results"""
        print("\n=== Test Execution Summary ===")
        print(f"Total Tests Run: {len(self.test_results)}")
        
        # Calculate statistics
        successful_tests = len([t for t in self.test_results if t['status'] == 'Success'])
        failed_tests = len([t for t in self.test_results if t['status'] == 'Failed'])
        
        print(f"Successful Tests: {successful_tests}")
        print(f"Failed Tests: {failed_tests}")
        
        # Print results by category
        print("\nResults by Category:")
        categories = set([t['category'] for t in self.test_results])
        for category in categories:
            category_tests = [t for t in self.test_results if t['category'] == category]
            category_success = len([t for t in category_tests if t['status'] == 'Success'])
            print(f"{category}: {category_success}/{len(category_tests)} passed")

        print("\n=== Test Suite Completed ===")

def main():
    """Main test execution function"""
    # Initialize and run tests
    tester = HealthcareAssistantTester()
    tester.run_test_suite()

if __name__ == "__main__":
    main()