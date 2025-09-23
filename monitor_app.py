#!/usr/bin/env python3
"""
Simple App Monitor
Checks if the app is running and provides restart instructions
"""

import requests
import time
import subprocess
import sys

def check_app():
    """Check if the app is running"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=3)
        return response.status_code == 200
    except:
        return False

def restart_app():
    """Restart the Flask app"""
    print("🔄 Restarting Flask app...")
    try:
        # Kill existing Python processes
        subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                      capture_output=True, check=False)
        time.sleep(2)
        
        # Start the app
        subprocess.Popen([sys.executable, 'app_educational_video.py'])
        print("✅ App restarted! Please wait 5-10 seconds for it to fully start.")
        return True
    except Exception as e:
        print(f"❌ Error restarting app: {e}")
        return False

def main():
    """Main monitoring loop"""
    print("🔍 Math Visualization Generator Monitor")
    print("=" * 40)
    
    while True:
        if check_app():
            print("✅ App is running normally")
        else:
            print("❌ App is not responding!")
            print("🔄 Attempting to restart...")
            if restart_app():
                print("⏳ Waiting for app to start...")
                time.sleep(10)
            else:
                print("❌ Failed to restart. Please restart manually.")
        
        print("Press Ctrl+C to stop monitoring")
        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped.")
