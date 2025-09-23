#!/usr/bin/env python3
"""Check the latest enhanced video for audio"""

from moviepy.editor import VideoFileClip
import os

def check_latest_video():
    """Check the latest enhanced video for audio"""
    video_path = "outputs/enhanced_educational_solution_931ae37f-17ab-4b79-9e58-5d45a7f5fe39.mp4"
    
    if os.path.exists(video_path):
        try:
            vc = VideoFileClip(video_path)
            print(f"Video: {video_path}")
            print(f"Duration: {vc.duration:.2f} seconds")
            print(f"Has audio: {vc.audio is not None}")
            
            if vc.audio:
                print(f"Audio duration: {vc.audio.duration:.2f} seconds")
                print(f"Audio fps: {vc.audio.fps}")
                print("✅ SUCCESS: Video has audio!")
            else:
                print("❌ FAILURE: Video has no audio")
            
            vc.close()
        except Exception as e:
            print(f"Error checking video: {e}")
    else:
        print(f"Video file not found: {video_path}")

if __name__ == "__main__":
    check_latest_video()
