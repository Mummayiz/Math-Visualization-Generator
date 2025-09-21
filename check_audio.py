#!/usr/bin/env python3
"""Check if video has audio"""

from moviepy.editor import VideoFileClip
import os

def check_video_audio(video_path):
    """Check if a video file has audio"""
    try:
        vc = VideoFileClip(video_path)
        print(f"Video: {video_path}")
        print(f"Duration: {vc.duration:.2f} seconds")
        print(f"Has audio: {vc.audio is not None}")
        
        if vc.audio:
            print(f"Audio duration: {vc.audio.duration:.2f} seconds")
            print(f"Audio fps: {vc.audio.fps}")
        else:
            print("No audio track found")
        
        vc.close()
        return vc.audio is not None
    except Exception as e:
        print(f"Error checking {video_path}: {e}")
        return False

if __name__ == "__main__":
    # Check the latest video
    video_path = "outputs/math_solution_general.mp4"
    if os.path.exists(video_path):
        check_video_audio(video_path)
    else:
        print(f"Video file {video_path} not found")
        
    # Check all videos
    print("\n=== ALL VIDEOS ===")
    for file in os.listdir("outputs"):
        if file.endswith(".mp4"):
            check_video_audio(f"outputs/{file}")
            print()
