import requests
import os
import time

def test_final():
    # Test the upload endpoint with the test image
    url = 'http://localhost:5000/upload'
    files = {'image': open('test_math.png', 'rb')}

    try:
        response = requests.post(url, files=files)
        print('Upload response:', response.status_code)
        if response.status_code == 200:
            result = response.json()
            print('Task ID:', result.get('task_id'))
            print('Message:', result.get('message'))
            
            # Check progress multiple times
            task_id = result.get('task_id')
            for i in range(15):
                time.sleep(2)
                progress_url = f'http://localhost:5000/progress/{task_id}'
                progress_response = requests.get(progress_url)
                if progress_response.status_code == 200:
                    progress_data = progress_response.json()
                    print(f'Progress: {progress_data.get("progress", 0)}% - {progress_data.get("message", "")}')
                    if progress_data.get('status') == 'completed':
                        result_data = progress_data.get('result', {})
                        print('✅ Video path:', result_data.get('video_path'))
                        print('✅ Success:', result_data.get('success'))
                        break
                    elif progress_data.get('status') == 'error':
                        print('❌ Error:', progress_data.get('message'))
                        break
                else:
                    print(f'Error: {progress_response.status_code}')
        else:
            print('Error:', response.text)
    except Exception as e:
        print('Error:', e)
    finally:
        files['image'].close()

if __name__ == '__main__':
    test_final()
