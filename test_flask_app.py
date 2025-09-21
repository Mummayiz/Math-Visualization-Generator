#!/usr/bin/env python3
"""Test the Flask app's video generation logic"""

from app_educational_video import enhanced_video_generator, video_generator
import traceback

def test_flask_video_generation():
    """Test the Flask app's video generation logic"""
    try:
        # This is the actual data structure from the Flask app
        problem_info = {
            'original_text': 'Math Prob1em 50 + 5 = ? 5o1ve this addition prob1em step by step What is 50 + 5?',
            'problem_type': 'general',
            'complexity': 'intermediate',
            'equations': ['Math Prob1em 50 + 5 = ? 5o1ve this addition prob1em step by step What is 50 + 5?', 'Math Prob1em 50 + 5 = ? 5o1ve this addition prob1em step by step What is 50 + 5?'],
            'expressions': ['50 + 5', '50 + 5'],
            'instructions': [],
            'variables': []
        }
        
        solution = {
            'problem_type': 'general',
            'steps': [
                {'step_number': 1, 'description': '**1. Step-by-step solution:**', 'equation': '', 'explanation': '', 'step_number': 1},
                {'step_number': 2, 'description': "* **Step 1: Identify the place values.**  The number 50 has a '5' in the tens place (representing 5 tens or 50 ones) and a '0' in the ones place. The number 5 has a '5' in the ones place.", 'equation': '', 'explanation': '', 'step_number': 2},
                {'step_number': 3, 'description': '* **Step 2: Add the ones digits.** We add the digits in the ones column: 0 + 5 = 5.  This result (5) becomes the ones digit of the sum.', 'equation': '', 'explanation': '', 'step_number': 3},
                {'step_number': 4, 'description': "* **Step 3: Add the tens digits.**  There is a '5' in the tens place of 50, and there are no tens in the number 5. So we simply carry over the '5' from the tens place of 50. This becomes the tens digit of the sum.", 'equation': '', 'explanation': '', 'step_number': 4},
                {'step_number': 5, 'description': '* **Step 4: Combine the results.** We combine the results from steps 2 and 3 to get the final answer. The tens digit is 5 and the ones digit is 5.', 'equation': '', 'explanation': '', 'step_number': 5}
            ],
            'final_answer': 'Therefore, the solution is correct.',
            'explanation': []
        }
        
        task_id = 'test_flask_app'
        
        print("Testing Flask app's enhanced video generation...")
        print(f"Enhanced video generator audio enabled: {enhanced_video_generator.audio_enabled}")
        
        try:
            video_filename = enhanced_video_generator.generate_educational_video(problem_info, solution, task_id)
            print(f"✅ Enhanced video generation result: {video_filename}")
        except Exception as e:
            print(f"❌ Enhanced video generation failed: {e}")
            traceback.print_exc()
            # Fallback to regular video generator
            try:
                video_filename = video_generator.generate_educational_video(problem_info, solution, task_id)
                print(f"🎬 Fallback video generation result: {video_filename}")
            except Exception as e2:
                print(f"❌ Fallback video generation also failed: {e2}")
                video_filename = None
        
        if video_filename:
            # Check if it has audio
            from moviepy.editor import VideoFileClip
            vc = VideoFileClip(f'outputs/{video_filename}')
            print(f"Duration: {vc.duration}")
            print(f"Has audio: {vc.audio is not None}")
            vc.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_flask_video_generation()
