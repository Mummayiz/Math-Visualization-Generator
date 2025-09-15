#!/usr/bin/env python3
"""
Fast and Accurate Video Generator for Math Problem Solver
Simple, no animations, maximum speed and accuracy
"""

import os
from typing import Dict, List, Any, Optional
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from config import Config

# Import moviepy for video generation
from moviepy.editor import *

class VideoGenerator:
    """Fast and accurate video generator without animations"""
    
    def __init__(self):
        self.config = Config()
        self.ensure_directories()
        
    def ensure_directories(self):
        """Create necessary directories"""
        Config.ensure_directories()
        
    def generate_video(self, problem_info: Dict[str, Any], solution: Dict[str, Any]) -> str:
        """Generate a fast, accurate video without animations"""
        
        print("Creating fast, accurate video...")
        
        # Create simple video clips
        clips = []
        
        # 1. Simple introduction
        print("Creating introduction...")
        intro_clip = self._create_simple_intro(problem_info)
        clips.append(intro_clip)
        
        # 2. Problem presentation
        print("Creating problem slide...")
        problem_clip = self._create_simple_problem(problem_info)
        clips.append(problem_clip)
        
        # 3. Solution steps
        print("Creating solution steps...")
        for i, step in enumerate(solution.get('steps', []), 1):
            print(f"Creating step {i}...")
            step_clip = self._create_simple_step(step, i, len(solution.get('steps', [])))
            clips.append(step_clip)
        
        # 4. Conclusion
        print("Creating conclusion...")
        conclusion_clip = self._create_simple_conclusion(solution)
        clips.append(conclusion_clip)
        
        # Concatenate all clips
        print("Combining clips...")
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Generate output filename
        output_filename = f"math_solution_{problem_info.get('problem_type', 'general')}.mp4"
        output_path = os.path.join(self.config.OUTPUT_FOLDER, output_filename)
        
        # Write video file with maximum speed settings
        print("Rendering video (maximum speed)...")
        final_video.write_videofile(
            output_path,
            fps=15,  # Lower FPS for speed
            codec='libx264',
            preset='ultrafast',
            verbose=False,
            logger=None,
            write_logfile=False
        )
        
        print(f"Fast video created: {output_path}")
        return output_filename
    
    def _create_simple_intro(self, problem_info: Dict[str, Any]) -> VideoClip:
        """Create simple introduction slide"""
        
        def make_frame(t):
            img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Simple title
            title = "Math Problem Solver"
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), title, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (self.config.VIDEO_WIDTH - text_width) // 2
            y = (self.config.VIDEO_HEIGHT - text_height) // 2 - 100
            
            draw.text((x, y), title, fill='black', font=font)
            
            # Problem type
            problem_type = problem_info.get('problem_type', 'general')
            subtitle = f"{problem_type.title()} Problem"
            try:
                subtitle_font = ImageFont.truetype("arial.ttf", 40)
            except:
                subtitle_font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            text_width = bbox[2] - bbox[0]
            x = (self.config.VIDEO_WIDTH - text_width) // 2
            y += text_height + 50
            
            draw.text((x, y), subtitle, fill='blue', font=subtitle_font)
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=2)
    
    def _create_simple_problem(self, problem_info: Dict[str, Any]) -> VideoClip:
        """Create simple problem slide"""
        
        def make_frame(t):
            img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'lightblue')
            draw = ImageDraw.Draw(img)
            
            # Title
            title = "Problem:"
            try:
                title_font = ImageFont.truetype("arial.ttf", 50)
            except:
                title_font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), title, font=title_font)
            text_width = bbox[2] - bbox[0]
            draw.text(((self.config.VIDEO_WIDTH - text_width) // 2, 100), 
                     title, fill='black', font=title_font)
            
            # Problem text
            problem_text = problem_info.get('original_text', 'No problem provided')
            try:
                text_font = ImageFont.truetype("arial.ttf", 36)
            except:
                text_font = ImageFont.load_default()
            
            # Wrap text
            words = problem_text.split()
            lines = []
            current_line = []
            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                bbox = draw.textbbox((0, 0), test_line, font=text_font)
                if bbox[2] - bbox[0] > self.config.VIDEO_WIDTH - 100:
                    if len(current_line) > 1:
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
                        current_line = []
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw lines
            for i, line in enumerate(lines[:5]):  # Limit to 5 lines
                y_pos = 200 + i * 50
                bbox = draw.textbbox((0, 0), line, font=text_font)
                text_width = bbox[2] - bbox[0]
                x = (self.config.VIDEO_WIDTH - text_width) // 2
                draw.text((x, y_pos), line, fill='black', font=text_font)
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=3)
    
    def _create_simple_step(self, step: Dict[str, Any], step_number: int, total_steps: int) -> VideoClip:
        """Create simple step slide"""
        
        def make_frame(t):
            img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Step header
            step_title = f"Step {step_number} of {total_steps}"
            try:
                header_font = ImageFont.truetype("arial.ttf", 40)
            except:
                header_font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), step_title, font=header_font)
            text_width = bbox[2] - bbox[0]
            draw.text(((self.config.VIDEO_WIDTH - text_width) // 2, 50), 
                     step_title, fill='blue', font=header_font)
            
            # Step description
            description = step.get('description', '')
            if description:
                try:
                    desc_font = ImageFont.truetype("arial.ttf", 28)
                except:
                    desc_font = ImageFont.load_default()
                
                # Wrap text
                words = description.split()
                lines = []
                current_line = []
                for word in words:
                    current_line.append(word)
                    test_line = ' '.join(current_line)
                    bbox = draw.textbbox((0, 0), test_line, font=desc_font)
                    if bbox[2] - bbox[0] > self.config.VIDEO_WIDTH - 100:
                        if len(current_line) > 1:
                            current_line.pop()
                            lines.append(' '.join(current_line))
                            current_line = [word]
                        else:
                            lines.append(word)
                            current_line = []
                if current_line:
                    lines.append(' '.join(current_line))
                
                # Draw lines
                for i, line in enumerate(lines[:4]):  # Limit to 4 lines
                    y_pos = 120 + i * 40
                    draw.text((60, y_pos), line, fill='black', font=desc_font)
            
            # Step explanation
            explanation = step.get('explanation', '')
            if explanation:
                try:
                    exp_font = ImageFont.truetype("arial.ttf", 22)
                except:
                    exp_font = ImageFont.load_default()
                
                # Wrap text
                words = explanation.split()
                lines = []
                current_line = []
                for word in words:
                    current_line.append(word)
                    test_line = ' '.join(current_line)
                    bbox = draw.textbbox((0, 0), test_line, font=exp_font)
                    if bbox[2] - bbox[0] > self.config.VIDEO_WIDTH - 100:
                        if len(current_line) > 1:
                            current_line.pop()
                            lines.append(' '.join(current_line))
                            current_line = [word]
                        else:
                            lines.append(word)
                            current_line = []
                if current_line:
                    lines.append(' '.join(current_line))
                
                # Draw lines
                for i, line in enumerate(lines[:6]):  # Limit to 6 lines
                    y_pos = 300 + i * 30
                    draw.text((60, y_pos), line, fill='darkgreen', font=exp_font)
            
            return np.array(img)
        
        # Simple duration based on content length
        content_length = len(step.get('description', '')) + len(step.get('explanation', ''))
        duration = max(2, min(5, content_length // 50))  # 2-5 seconds based on content
        return VideoClip(make_frame, duration=duration)
    
    def _create_simple_conclusion(self, solution: Dict[str, Any]) -> VideoClip:
        """Create simple conclusion slide"""
        
        def make_frame(t):
            img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'lightgreen')
            draw = ImageDraw.Draw(img)
            
            # Title
            title = "Solution Complete!"
            try:
                font = ImageFont.truetype("arial.ttf", 50)
            except:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), title, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (self.config.VIDEO_WIDTH - text_width) // 2
            y = (self.config.VIDEO_HEIGHT - text_height) // 2 - 100
            
            draw.text((x, y), title, fill='black', font=font)
            
            # Final answer
            final_answer = solution.get('final_answer', 'No answer available')
            answer_text = f"Final Answer: {final_answer}"
            try:
                answer_font = ImageFont.truetype("arial.ttf", 36)
            except:
                answer_font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), answer_text, font=answer_font)
            text_width = bbox[2] - bbox[0]
            x = (self.config.VIDEO_WIDTH - text_width) // 2
            y += text_height + 50
            
            draw.text((x, y), answer_text, fill='darkblue', font=answer_font)
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=3)
