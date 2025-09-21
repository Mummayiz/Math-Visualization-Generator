#!/usr/bin/env python3
"""
Test the system with a real math problem image
"""

import requests
import time
import json

def test_real_math_problem():
    """Test with a real math problem image"""
    
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
        print(f"Message: {data.get('message')}")
        
        # Poll for progress
        while True:
            progress_url = f"http://localhost:5000/progress/{task_id}"
            progress_response = requests.get(progress_url)
            
            if progress_response.status_code == 200:
                progress_data = progress_response.json()
                progress = progress_data.get("progress", 0)
                message = progress_data.get("message", "")
                status = progress_data.get("status", "")
                
                print(f"Progress: {progress}% - {message}")
                
                if status == "completed":
                    result = progress_data.get("result", {})
                    print(f"✅ Video path: {result.get('video_path')}")
                    print(f"✅ Success: {result.get('success')}")
                    
                    # Print the extracted text and problem info
                    print(f"📝 Extracted text: {result.get('extracted_text', 'N/A')}")
                    problem_info = result.get('problem_info', {})
                    print(f"📊 Problem type: {problem_info.get('problem_type', 'N/A')}")
                    print(f"🧮 Complexity: {problem_info.get('complexity', 'N/A')}")
                    
                    # Print solution steps
                    solution = result.get('solution', {})
                    steps = solution.get('steps', [])
                    print(f"🔧 Solution steps ({len(steps)}):")
                    for i, step in enumerate(steps[:3], 1):  # Show first 3 steps
                        if isinstance(step, dict):
                            print(f"  Step {i}: {step.get('description', 'N/A')}")
                        else:
                            print(f"  Step {i}: {step}")
                    
                    break
                elif status == "error":
                    print(f"❌ Error: {message}")
                    break
            else:
                print(f"❌ Progress check failed: {progress_response.status_code}")
                break
            
            time.sleep(1)
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_real_math_problem()
