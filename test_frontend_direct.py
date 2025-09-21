#!/usr/bin/env python3
"""
Test the frontend directly by making a request and checking the response
"""

import requests
import time
import json

def test_frontend_direct():
    """Test the frontend by uploading an image and checking the response"""
    
    # Upload the real math problem image
    url = "http://localhost:5000/upload"
    
    with open("test_math_problem.png", "rb") as f:
        files = {"image": ("test_math_problem.png", f, "image/png")}
        data = {"fast_mode": "false"}
        response = requests.post(url, files=files, data=data)
    
    print(f"Upload response: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        task_id = data.get("task_id")
        print(f"Task ID: {task_id}")
        
        # Poll for progress until completion
        while True:
            progress_url = f"http://localhost:5000/progress/{task_id}"
            progress_response = requests.get(progress_url)
            
            if progress_response.status_code == 200:
                progress_data = progress_response.json()
                status = progress_data.get("status", "")
                
                if status == "completed":
                    result = progress_data.get("result", {})
                    print("\n=== FRONTEND SHOULD RECEIVE ===")
                    print(f"Success: {result.get('success')}")
                    print(f"Extracted text: {result.get('extracted_text', 'N/A')}")
                    print(f"Problem type: {result.get('problem_info', {}).get('problem_type', 'N/A')}")
                    print(f"Complexity: {result.get('problem_info', {}).get('complexity', 'N/A')}")
                    print(f"Video path: {result.get('video_path', 'N/A')}")
                    
                    # Test the frontend page directly
                    print("\n=== TESTING FRONTEND PAGE ===")
                    frontend_response = requests.get("http://localhost:5000/")
                    print(f"Frontend response: {frontend_response.status_code}")
                    
                    if frontend_response.status_code == 200:
                        print("✅ Frontend page is accessible")
                        # Check if the page contains the expected elements
                        content = frontend_response.text
                        if "extractedText" in content:
                            print("✅ Frontend contains extractedText element")
                        else:
                            print("❌ Frontend missing extractedText element")
                        
                        if "problemType" in content:
                            print("✅ Frontend contains problemType element")
                        else:
                            print("❌ Frontend missing problemType element")
                    else:
                        print("❌ Frontend page not accessible")
                    
                    break
                elif status == "error":
                    print(f"❌ Error: {progress_data.get('message')}")
                    break
            else:
                print(f"❌ Progress check failed: {progress_response.status_code}")
                break
            
            time.sleep(1)
    else:
        print(f"❌ Upload failed: {response.status_code}")

if __name__ == "__main__":
    test_frontend_direct()
