#!/usr/bin/env python3
"""
Test if there's a browser caching issue by checking the frontend response
"""

import requests
import time

def test_browser_cache():
    """Test if the frontend is serving the updated content"""
    
    # Test the frontend page
    print("=== TESTING FRONTEND CACHE ===")
    
    # Make multiple requests to see if content changes
    for i in range(3):
        response = requests.get(f"http://localhost:5000/?v={time.time()}")
        print(f"Request {i+1}: Status {response.status_code}")
        
        # Check if the page contains the updated JavaScript
        content = response.text
        if "data.extracted_text" in content:
            print(f"✅ Request {i+1}: Contains updated JavaScript")
        else:
            print(f"❌ Request {i+1}: Missing updated JavaScript")
        
        if "data.problem_info?.problem_type" in content:
            print(f"✅ Request {i+1}: Contains updated problem type handling")
        else:
            print(f"❌ Request {i+1}: Missing updated problem type handling")
        
        time.sleep(1)
    
    print("\n=== TESTING UPLOAD AND PROGRESS ===")
    
    # Upload an image and check progress
    with open("test_math_problem.png", "rb") as f:
        files = {"image": ("test_math_problem.png", f, "image/png")}
        data = {"fast_mode": "false"}
        response = requests.post("http://localhost:5000/upload", files=files, data=data)
    
    if response.status_code == 200:
        task_id = response.json().get("task_id")
        print(f"✅ Upload successful, task ID: {task_id}")
        
        # Check progress
        progress_response = requests.get(f"http://localhost:5000/progress/{task_id}")
        if progress_response.status_code == 200:
            progress_data = progress_response.json()
            print(f"✅ Progress check successful")
            print(f"Status: {progress_data.get('status')}")
            print(f"Progress: {progress_data.get('progress')}%")
            print(f"Message: {progress_data.get('message')}")
            
            if progress_data.get('status') == 'completed':
                result = progress_data.get('result', {})
                print(f"✅ Processing completed")
                print(f"Extracted text: {result.get('extracted_text', 'N/A')}")
                print(f"Problem type: {result.get('problem_info', {}).get('problem_type', 'N/A')}")
                print(f"Video path: {result.get('video_path', 'N/A')}")
        else:
            print(f"❌ Progress check failed: {progress_response.status_code}")
    else:
        print(f"❌ Upload failed: {response.status_code}")

if __name__ == "__main__":
    test_browser_cache()
