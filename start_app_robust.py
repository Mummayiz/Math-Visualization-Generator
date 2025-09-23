#!/usr/bin/env python3
"""
Robust Flask App Starter
Automatically restarts the app when it crashes or stops responding
"""

import subprocess
import time
import requests
import sys
import os

def check_app_health():
    """Check if the Flask app is responding"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        return response.status_code == 200
    except:
        return False

def start_app():
    """Start the Flask app"""
    print("🚀 Starting Math Visualization Generator...")
    try:
        # Start the app in the background
        process = subprocess.Popen([
            sys.executable, 'app_educational_video.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        return None

def main():
    """Main loop to keep the app running"""
    print("🎓 Math Visualization Generator - Robust Starter")
    print("=" * 50)
    
    process = None
    restart_count = 0
    
    while True:
        try:
            # Check if app is running and healthy
            if process is None or process.poll() is not None:
                print(f"\n🔄 {'Restarting' if process else 'Starting'} app... (Attempt #{restart_count + 1})")
                
                # Kill any existing processes on port 5000
                try:
                    subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                                 capture_output=True, check=False)
                    time.sleep(2)
                except:
                    pass
                
                # Start the app
                process = start_app()
                if process is None:
                    print("❌ Failed to start app, retrying in 10 seconds...")
                    time.sleep(10)
                    continue
                
                restart_count += 1
                print("⏳ Waiting for app to start...")
                time.sleep(5)
            
            # Check if app is responding
            if check_app_health():
                print("✅ App is running and healthy!")
                print("🌐 Access at: http://localhost:5000")
                print("📱 Press Ctrl+C to stop")
                
                # Wait and check periodically
                time.sleep(10)
            else:
                print("⚠️  App not responding, restarting...")
                if process:
                    process.terminate()
                    process = None
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping app...")
            if process:
                process.terminate()
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            if process:
                process.terminate()
                process = None
            time.sleep(5)

if __name__ == "__main__":
    main()
