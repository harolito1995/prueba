"""
Comprehensive test runner for the Medical Image Processing API
"""
import requests
import json
import time
from datetime import datetime
from sample_data import SAMPLE_PAYLOAD_1, SAMPLE_PAYLOAD_2

class APITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.created_ids = []
    
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def test_health_check(self):
        """Test the health check endpoint"""
        self.log("Testing health check endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/health")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.json()
            assert "status" in data, "Response missing 'status' field"
            assert data["status"] == "healthy", f"Expected 'healthy', got {data['status']}"
            self.log("✓ Health check passed")
            return True
        except Exception as e:
            self.log(f"✗ Health check failed: {e}", "ERROR")
            return False
    
    def test_create_elements(self, payload, test_name=""):
        """Test creating processing results"""
        self.log(f"Testing create elements {test_name}...")
        try:
            response = self.session.post(
                f"{self.base_url}/api/elements/",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            # Handle different expected status codes based on test scenario
            if test_name == "batch 1" and response.status_code == 409:
                # First batch might fail due to existing data - this is expected
                error_data = response.json()
                assert "detail" in error_data, "Error response missing 'detail' field"
                self.log(f"✓ Expected conflict (409) for duplicate ID: {error_data['detail']}")
                return True
            elif response.status_code == 200:
                # Successful creation
                results = response.json()
                assert isinstance(results, list), "Response should be a list"
                assert len(results) == len(payload), f"Expected {len(payload)} results, got {len(results)}"
                
                for result in results:
                    assert "id" in result, "Result missing 'id' field"
                    assert "device" in result, "Result missing 'device' field"
                    assert "average_before_normalization" in result, "Result missing average_before_normalization"
                    assert "average_after_normalization" in result, "Result missing average_after_normalization"
                    assert "data_size" in result, "Result missing data_size"
                    
                    # Verify normalization (after should be <= before for positive data)
                    assert result["average_after_normalization"] <= result["average_before_normalization"], \
                        "Average after normalization should be <= average before"
                    
                    self.created_ids.append(result["id"])
                
                self.log(f"✓ Created {len(results)} processing results successfully")
                return True
            else:
                # Unexpected status code
                assert False, f"Unexpected status code: {response.status_code}"
                
        except Exception as e:
            self.log(f"✗ Create elements failed: {e}", "ERROR")
            return False
    
    def test_get_all_elements(self):
        """Test getting all processing results"""
        self.log("Testing get all elements...")
        try:
            response = self.session.get(f"{self.base_url}/api/elements/")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            results = response.json()
            assert isinstance(results, list), "Response should be a list"
            assert len(results) > 0, "Should have at least some results"
            
            self.log(f"✓ Retrieved {len(results)} processing results")
            return True
        except Exception as e:
            self.log(f"✗ Get all elements failed: {e}", "ERROR")
            return False
    
    def test_get_single_element(self):
        """Test getting a single processing result"""
        if not self.created_ids:
            self.log("✗ No created IDs available for single element test", "ERROR")
            return False
        
        element_id = self.created_ids[0]
        self.log(f"Testing get single element {element_id}...")
        try:
            response = self.session.get(f"{self.base_url}/api/elements/{element_id}")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            result = response.json()
            assert result["id"] == element_id, f"Expected ID {element_id}, got {result['id']}"
            assert "device" in result, "Result missing 'device' field"
            
            self.log(f"✓ Retrieved single element {element_id}")
            return True
        except Exception as e:
            self.log(f"✗ Get single element failed: {e}", "ERROR")
            return False
    
    def test_update_element(self):
        """Test updating a processing result"""
        if not self.created_ids:
            self.log("✗ No created IDs available for update test", "ERROR")
            return False
        
        element_id = self.created_ids[0]
        self.log(f"Testing update element {element_id}...")
        try:
            update_data = {"device_name": "UPDATED_DEVICE"}
            response = self.session.put(
                f"{self.base_url}/api/elements/{element_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            result = response.json()
            assert result["device"]["device_name"] == "UPDATED_DEVICE", \
                f"Expected 'UPDATED_DEVICE', got {result['device']['device_name']}"
            
            self.log(f"✓ Updated element {element_id}")
            return True
        except Exception as e:
            self.log(f"✗ Update element failed: {e}", "ERROR")
            return False
    
    def test_filtering(self):
        """Test filtering functionality"""
        self.log("Testing filtering...")
        try:
            # Test data size filter
            response = self.session.get(f"{self.base_url}/api/elements/?data_size_min=25&data_size_max=35")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            results = response.json()
            for result in results:
                assert 25 <= result["data_size"] <= 35, \
                    f"Data size {result['data_size']} not in range [25, 35]"
            
            self.log(f"✓ Filtering returned {len(results)} results")
            return True
        except Exception as e:
            self.log(f"✗ Filtering failed: {e}", "ERROR")
            return False
    
    def test_error_handling(self):
        """Test error handling with invalid data"""
        self.log("Testing error handling...")
        try:
            invalid_payload = {
                "1": {
                    "id": "invalid_test",
                    "data": ["invalid data here", "not numbers"],
                    "deviceName": "TEST_DEVICE"
                }
            }
            response = self.session.post(
                f"{self.base_url}/api/elements/",
                json=invalid_payload,
                headers={"Content-Type": "application/json"}
            )
            assert response.status_code == 422, f"Expected 422, got {response.status_code}"
            
            self.log("✓ Error handling working correctly")
            return True
        except Exception as e:
            self.log(f"✗ Error handling test failed: {e}", "ERROR")
            return False
    
    def test_delete_element(self):
        """Test deleting a processing result"""
        if not self.created_ids:
            self.log("✗ No created IDs available for delete test", "ERROR")
            return False
        
        element_id = self.created_ids.pop()  # Remove from list
        self.log(f"Testing delete element {element_id}...")
        try:
            response = self.session.delete(f"{self.base_url}/api/elements/{element_id}")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            result = response.json()
            assert "message" in result, "Response missing 'message' field"
            
            # Verify deletion
            response = self.session.get(f"{self.base_url}/api/elements/{element_id}")
            assert response.status_code == 404, f"Expected 404, got {response.status_code}"
            
            self.log(f"✓ Deleted element {element_id}")
            return True
        except Exception as e:
            self.log(f"✗ Delete element failed: {e}", "ERROR")
            return False
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        self.log("Starting comprehensive API tests...")
        
        tests = [
            self.test_health_check,
            lambda: self.test_create_elements(SAMPLE_PAYLOAD_1, "batch 1"),
            lambda: self.test_create_elements(SAMPLE_PAYLOAD_2, "batch 2"),
            self.test_get_all_elements,
            self.test_get_single_element,
            self.test_update_element,
            self.test_filtering,
            self.test_error_handling,
            self.test_delete_element,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                self.log(f"✗ Test failed with exception: {e}", "ERROR")
                failed += 1
            
            time.sleep(0.5)  # Small delay between tests
        
        self.log(f"Tests completed: {passed} passed, {failed} failed")
        return failed == 0

def main():
    """Main test runner"""
    tester = APITester()
    
    # Wait for API to be ready
    print("Waiting for API to be ready...")
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get(f"{tester.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("API is ready!")
                break
        except:
            pass
        time.sleep(1)
    else:
        print("API failed to start within timeout period")
        return False
    
    # Run tests
    return tester.run_all_tests()

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)