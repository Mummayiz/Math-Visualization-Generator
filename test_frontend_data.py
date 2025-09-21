#!/usr/bin/env python3
"""
Test the frontend data structure by simulating what the backend sends
"""

import requests
import time
import json

def test_frontend_data():
    """Test what data the frontend receives"""
    
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
                    print("\n=== FRONTEND DATA STRUCTURE ===")
                    print(f"Success: {result.get('success')}")
                    print(f"Extracted text: {result.get('extracted_text', 'N/A')}")
                    print(f"Problem info: {result.get('problem_info', {})}")
                    print(f"Solution: {result.get('solution', {})}")
                    print(f"Video path: {result.get('video_path', 'N/A')}")
                    print(f"Video filename: {result.get('video_filename', 'N/A')}")
                    
                    # Check what the frontend will see
                    print("\n=== FRONTEND MAPPING ===")
                    print(f"data.extracted_text: {result.get('extracted_text', 'N/A')}")
                    print(f"data.problem_info?.problem_type: {result.get('problem_info', {}).get('problem_type', 'N/A')}")
                    print(f"data.problem_info?.complexity: {result.get('problem_info', {}).get('complexity', 'N/A')}")
                    print(f"data.video_path: {result.get('video_path', 'N/A')}")
                    
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
    test_frontend_data()
