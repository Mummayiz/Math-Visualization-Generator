#!/usr/bin/env python3
"""Test the enhanced video generator directly"""

from enhanced_educational_video_generator import EnhancedEducationalVideoGenerator
import traceback

def test_enhanced_video():
    """Test enhanced video generation"""
    try:
        evg = EnhancedEducationalVideoGenerator()
        
        problem_info = {
            'original_text': '50 + 5 = ?',
            'problem_type': 'arithmetic',
            'complexity': 'simple'
        }
        
        solution = {
            'steps': [
                {
                    'step_number': 1,
                    'description': 'Add 50 and 5',
                    'equation': '50 + 5 = 55'
                }
            ],
            'final_answer': '55'
        }
        
        print("Testing enhanced video generator...")
        result = evg.generate_educational_video(problem_info, solution, 'test_direct')
        print(f"✅ Video generated: {result}")
        
        # Check if it has audio
        from moviepy.editor import VideoFileClip
        vc = VideoFileClip(f'outputs/{result}')
        print(f"Duration: {vc.duration}")
        print(f"Has audio: {vc.audio is not None}")
        vc.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_enhanced_video()
