import requests
import json
import sys
import time

BASE_URL = "http://127.0.0.1:8780"

def test_endpoint(method, path, data=None, description=""):
    url = f"{BASE_URL}{path}"
    try:
        if method == "POST":
            resp = requests.post(url, json=data, timeout=2)
        else:
            resp = requests.get(url, timeout=2)
        ok = resp.status_code == 200
        print(f"{'✓' if ok else '✗'} {description} ({method} {path}) -> {resp.status_code}")
        if not ok:
            print(f"   Response: {resp.text[:200]}")
        return ok
    except Exception as e:
        print(f"✗ {description} ({method} {path}) -> Error: {e}")
        return False

def main():
    print("Testing HIMYM harness API endpoints...")
    print("Make sure the director is running on http://127.0.0.1:8780\n")
    
    all_passed = True
    
    # Test /api/auto
    all_passed &= test_endpoint("POST", "/api/auto", {"on": True}, "Enable auto mode")
    all_passed &= test_endpoint("POST", "/api/auto", {"on": False}, "Disable auto mode")
    
    # Test /api/speed
    all_passed &= test_endpoint("POST", "/api/speed", {"mult": 2.0, "paused": False}, "Set speed 2x")
    all_passed &= test_endpoint("POST", "/api/speed", {"mult": 1.0, "paused": True}, "Pause")
    
    # Test /api/control
    all_passed &= test_endpoint("POST", "/api/control", {"agent": "ted", "take": True}, "Take control of ted")
    all_passed &= test_endpoint("POST", "/api/control", {"agent": "ted", "release": True}, "Release control of ted")
    all_passed &= test_endpoint("POST", "/api/control", {"agent": "barney", "move": "LivingRoom", "status": "Working"}, "Set override for barney")
    all_passed &= test_endpoint("POST", "/api/control", {"agent": "lily", "task": "Fetch coffee"}, "Assign task via control")
    
    # Test /api/task
    all_passed &= test_endpoint("POST", "/api/task", {"text": "Test task from API"}, "Add task via /api/task")
    
    # Test /api/episode
    all_passed &= test_endpoint("POST", "/api/episode", {"id": "test_episode"}, "Start test episode")
    
    print(f"\n{'All tests passed!' if all_passed else 'Some tests failed!'}")
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
