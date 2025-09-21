#!/usr/bin/env python3
"""
Simple script to restart the educational video generator app
"""
import subprocess
import time
import sys
import os

def restart_app():
    print("🔄 Restarting Educational Math Video Generator...")
    
    # Kill any existing Python processes (be careful with this)
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                         capture_output=True, text=True)
        else:  # Unix/Linux/Mac
            subprocess.run(['pkill', '-f', 'app_educational_video.py'], 
                         capture_output=True, text=True)
        print("✅ Stopped existing processes")
    except Exception as e:
        print(f"⚠️  Could not stop existing processes: {e}")
    
    # Wait a moment
    time.sleep(2)
    
    # Start the app
    try:
        print("🚀 Starting app...")
        subprocess.Popen([sys.executable, 'app_educational_video.py'])
        print("✅ App started successfully!")
        print("🌐 App should be available at: http://localhost:5000")
    except Exception as e:
        print(f"❌ Failed to start app: {e}")

if __name__ == "__main__":
    restart_app()
