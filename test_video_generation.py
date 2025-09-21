#!/usr/bin/env python3
"""
Test video generation directly
"""

from educational_video_generator import EducationalVideoGenerator

# Test data
problem_info = {
    'type': 'arithmetic',
    'equation': '50 + 5 = ?',
    'num1': 50,
    'num2': 5,
    'operator': '+',
    'result': None
}

solution = {
    'answer': '55',
    'steps': [
        'Problem: 50 + 5 = ?',
        'Step 1: Identify the operation - this is addition',
        'Step 2: Apply the addition operation',
        'Step 3: 50 + 5 = 55',
        'Answer: 55'
    ],
    'final_answer': '55'
}

# Test video generation
video_generator = EducationalVideoGenerator()
video_filename = video_generator.generate_educational_video(problem_info, solution, 'test123')

print(f"Video generation result: {video_filename}")

# Check if file exists
import os
if video_filename and os.path.exists(f"outputs/{video_filename}"):
    print(f"✅ Video file created: outputs/{video_filename}")
    print(f"File size: {os.path.getsize(f'outputs/{video_filename}')} bytes")
else:
    print("❌ Video file not created")
