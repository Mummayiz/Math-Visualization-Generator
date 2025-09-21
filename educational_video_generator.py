#!/usr/bin/env python3
"""
Educational Video Generator for Math Problems
Creates step-by-step animated videos with clear explanations
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Any, Tuple
import json
import cv2

class EducationalVideoGenerator:
    """Generates educational videos with step-by-step math solutions"""
    
    def __init__(self, output_dir="outputs"):
        self.output_dir = output_dir
        self.width = 1200
        self.height = 800
        self.fps = 2  # 2 frames per second for smooth animation
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_educational_video(self, problem_info: Dict, solution: Dict, task_id: str) -> str:
        """Generate a comprehensive educational video"""
        try:
            print(f"🎬 Generating educational video for task {task_id}")
            
            # Create video frames
            frames = []
            
            # 1. Title and Problem Introduction (3 seconds)
            frames.extend(self._create_intro_frames(problem_info))
            
            # 2. Problem Analysis (2 seconds)
            frames.extend(self._create_analysis_frames(problem_info))
            
            # 3. Step-by-step Solution (variable length)
            frames.extend(self._create_solution_frames(solution))
            
            # 4. Final Answer and Summary (2 seconds)
            frames.extend(self._create_conclusion_frames(solution))
            
            if not frames:
                print("❌ No frames generated")
                return None
            
            print(f"📊 Generated {len(frames)} frames for video")
            
            # Save as MP4 video
            video_filename = f"educational_solution_{task_id}.mp4"
            video_path = os.path.join(self.output_dir, video_filename)
            
            # Convert frames to MP4 video
            if frames:
                height, width, layers = frames[0].shape
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                video_writer = cv2.VideoWriter(video_path, fourcc, self.fps, (width, height))
                
                # Write frames to video
                for frame in frames:
                    # Convert RGB to BGR for OpenCV
                    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    video_writer.write(frame_bgr)
                
                video_writer.release()
                print(f"✅ Educational video created: {video_filename} ({len(frames)} frames)")
                return video_filename
            else:
                print("❌ No valid frames to save")
                return None
            
        except Exception as e:
            print(f"❌ Video generation failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _create_intro_frames(self, problem_info: Dict) -> List[np.ndarray]:
        """Create introduction frames"""
        frames = []
        duration = 3 * self.fps  # 3 seconds
        
        for i in range(duration):
            img = Image.new('RGB', (self.width, self.height), color='#f0f8ff')
            draw = ImageDraw.Draw(img)
            
            try:
                title_font = ImageFont.truetype('arial.ttf', 48)
                subtitle_font = ImageFont.truetype('arial.ttf', 32)
                text_font = ImageFont.truetype('arial.ttf', 28)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
            
            # Animated title
            if i < duration // 2:
                alpha = int(255 * (i / (duration // 2)))
                title_color = (0, 0, 0, alpha)
            else:
                title_color = (0, 0, 0, 255)
            
            # Title
            draw.text((self.width//2 - 200, 100), "Math Problem Solver", 
                     fill=title_color, font=title_font)
            
            # Problem type
            problem_type = problem_info.get('problem_type', 'Mathematical Problem')
            draw.text((self.width//2 - 150, 200), f"Type: {problem_type}", 
                     fill=(0, 100, 200), font=subtitle_font)
            
            # Problem statement
            problem_text = problem_info.get('original_text', 'No problem provided')
            # Wrap text
            wrapped_text = self._wrap_text(problem_text, 50)
            y_pos = 300
            for line in wrapped_text[:3]:  # Show first 3 lines
                draw.text((50, y_pos), line, fill=(0, 0, 0), font=text_font)
                y_pos += 40
            
            frames.append(np.array(img))
        
        return frames
    
    def _create_analysis_frames(self, problem_info: Dict) -> List[np.ndarray]:
        """Create problem analysis frames"""
        frames = []
        duration = 2 * self.fps  # 2 seconds
        
        for i in range(duration):
            img = Image.new('RGB', (self.width, self.height), color='#fff8dc')
            draw = ImageDraw.Draw(img)
            
            try:
                header_font = ImageFont.truetype('arial.ttf', 36)
                text_font = ImageFont.truetype('arial.ttf', 24)
            except:
                header_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
            
            # Analysis header
            draw.text((50, 100), "🔍 Problem Analysis", fill=(139, 69, 19), font=header_font)
            
            # Problem breakdown
            analysis_points = [
                f"Problem Type: {problem_info.get('problem_type', 'Unknown')}",
                f"Variables: {self._extract_variables(problem_info.get('original_text', ''))}",
                f"Complexity: {self._assess_complexity(problem_info)}",
                "Strategy: Step-by-step algebraic manipulation"
            ]
            
            y_pos = 200
            for point in analysis_points:
                # Animate appearance
                if i > duration // 4:
                    draw.text((100, y_pos), f"• {point}", fill=(0, 0, 0), font=text_font)
                y_pos += 50
            
            frames.append(np.array(img))
        
        return frames
    
    def _create_solution_frames(self, solution: Dict) -> List[np.ndarray]:
        """Create step-by-step solution frames"""
        frames = []
        steps = solution.get('steps', [])
        
        if not steps or not isinstance(steps, list):
            # Fallback if no steps provided
            steps = ["Step 1: Analyze the problem", "Step 2: Apply mathematical principles", "Step 3: Solve"]
        
        # Ensure we have at least one step
        if not steps:
            steps = ["Step 1: Problem solving in progress"]
        
        for step_idx, step in enumerate(steps):
            # Each step gets 3 seconds of frames
            step_duration = 3 * self.fps
            
            for i in range(step_duration):
                img = Image.new('RGB', (self.width, self.height), color='#f0fff0')
                draw = ImageDraw.Draw(img)
                
                try:
                    step_font = ImageFont.truetype('arial.ttf', 40)
                    text_font = ImageFont.truetype('arial.ttf', 28)
                    small_font = ImageFont.truetype('arial.ttf', 20)
                except:
                    step_font = ImageFont.load_default()
                    text_font = ImageFont.load_default()
                    small_font = ImageFont.load_default()
                
                # Step header with animation
                step_title = f"Step {step_idx + 1}"
                if i < step_duration // 3:
                    # Fade in
                    alpha = int(255 * (i / (step_duration // 3)))
                    step_color = (0, 100, 0, alpha)
                else:
                    step_color = (0, 100, 0, 255)
                
                draw.text((50, 100), step_title, fill=step_color, font=step_font)
                
                # Step content
                if i > step_duration // 4:
                    # Wrap and display step text
                    wrapped_step = self._wrap_text(str(step), 60)
                    y_pos = 200
                    for line in wrapped_step[:4]:  # Show first 4 lines
                        draw.text((100, y_pos), line, fill=(0, 0, 0), font=text_font)
                        y_pos += 40
                
                # Visual elements
                if i > step_duration // 2:
                    # Draw mathematical symbols or diagrams
                    self._draw_step_visuals(draw, step_idx, step, i - step_duration // 2)
                
                # Progress indicator
                progress = (step_idx + 1) / len(steps)
                self._draw_progress_bar(draw, progress)
                
                frames.append(np.array(img))
        
        return frames
    
    def _create_conclusion_frames(self, solution: Dict) -> List[np.ndarray]:
        """Create conclusion frames"""
        frames = []
        duration = 2 * self.fps  # 2 seconds
        
        for i in range(duration):
            img = Image.new('RGB', (self.width, self.height), color='#e6ffe6')
            draw = ImageDraw.Draw(img)
            
            try:
                title_font = ImageFont.truetype('arial.ttf', 48)
                answer_font = ImageFont.truetype('arial.ttf', 36)
                text_font = ImageFont.truetype('arial.ttf', 24)
            except:
                title_font = ImageFont.load_default()
                answer_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
            
            # Conclusion title
            draw.text((self.width//2 - 150, 100), "✅ Solution Complete!", 
                     fill=(0, 150, 0), font=title_font)
            
            # Final answer
            final_answer = solution.get('final_answer', 'Solution completed')
            draw.text((self.width//2 - 200, 250), f"Final Answer: {final_answer}", 
                     fill=(200, 0, 0), font=answer_font)
            
            # Summary
            summary_text = [
                "Key concepts used:",
                "• Algebraic manipulation",
                "• Problem-solving strategies", 
                "• Mathematical reasoning"
            ]
            
            y_pos = 350
            for line in summary_text:
                draw.text((100, y_pos), line, fill=(0, 0, 0), font=text_font)
                y_pos += 40
            
            # Success animation
            if i > duration // 2:
                self._draw_success_animation(draw, i - duration // 2)
            
            frames.append(np.array(img))
        
        return frames
    
    def _wrap_text(self, text: str, max_width: int) -> List[str]:
        """Wrap text to fit within max_width characters"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > max_width:
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
                    current_line = []
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _extract_variables(self, text: str) -> str:
        """Extract mathematical variables from text"""
        import re
        variables = re.findall(r'[a-zA-Z]', text)
        unique_vars = list(set(variables))
        return ', '.join(unique_vars) if unique_vars else 'None detected'
    
    def _assess_complexity(self, problem_info: Dict) -> str:
        """Assess problem complexity"""
        problem_type = problem_info.get('problem_type', '')
        if isinstance(problem_type, dict):
            problem_type = str(problem_type)
        elif not isinstance(problem_type, str):
            problem_type = str(problem_type)
        
        problem_type_lower = problem_type.lower()
        if 'quadratic' in problem_type_lower:
            return 'Intermediate'
        elif 'linear' in problem_type_lower:
            return 'Basic'
        elif 'derivative' in problem_type_lower or 'integral' in problem_type_lower:
            return 'Advanced'
        else:
            return 'Moderate'
    
    def _draw_step_visuals(self, draw: ImageDraw.Draw, step_idx: int, step: str, frame: int):
        """Draw visual elements for each step"""
        # Ensure step is a string
        if not isinstance(step, str):
            step = str(step)
        
        step_lower = step.lower()
        # Draw mathematical symbols or diagrams based on step content
        if 'equation' in step_lower or '=' in step:
            # Draw equation line
            draw.line([(200, 400), (800, 400)], fill=(0, 0, 255), width=3)
        
        if 'add' in step_lower or '+' in step:
            # Draw plus symbol
            draw.text((500, 450), "+", fill=(0, 150, 0), font=ImageFont.load_default())
        
        if 'multiply' in step_lower or '*' in step:
            # Draw multiplication symbol
            draw.text((500, 450), "×", fill=(0, 150, 0), font=ImageFont.load_default())
    
    def _draw_progress_bar(self, draw: ImageDraw.Draw, progress: float):
        """Draw progress bar"""
        bar_width = 800
        bar_height = 20
        x = (self.width - bar_width) // 2
        y = self.height - 100
        
        # Background
        draw.rectangle([x, y, x + bar_width, y + bar_height], fill=(200, 200, 200))
        
        # Progress
        progress_width = int(bar_width * progress)
        draw.rectangle([x, y, x + progress_width, y + bar_height], fill=(0, 150, 0))
        
        # Text
        try:
            font = ImageFont.truetype('arial.ttf', 16)
        except:
            font = ImageFont.load_default()
        draw.text((x + bar_width + 20, y), f"{int(progress * 100)}%", fill=(0, 0, 0), font=font)
    
    def _draw_success_animation(self, draw: ImageDraw.Draw, frame: int):
        """Draw success animation"""
        # Draw checkmark
        center_x = self.width // 2
        center_y = 500
        
        if frame < 10:
            # Growing checkmark
            size = frame * 5
            draw.ellipse([center_x - size, center_y - size, center_x + size, center_y + size], 
                        fill=(0, 255, 0, 100))
