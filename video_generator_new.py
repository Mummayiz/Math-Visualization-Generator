#!/usr/bin/env python3
"""
Fast Visual Video Generator for Math Problem Solver
Generates animated educational videos with visual effects, no audio
"""

import os
import tempfile
from typing import Dict, List, Any, Optional
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io
from config import Config

# Import moviepy for video generation
from moviepy.editor import *

class VideoGenerator:
    """Fast video generator with visual animations and effects"""
    
    def __init__(self):
        self.config = Config()
        self.ensure_directories()
        
    def ensure_directories(self):
        """Create necessary directories"""
        Config.ensure_directories()
        
    def generate_video(self, problem_info: Dict[str, Any], solution: Dict[str, Any]) -> str:
        """Generate a fast visual educational video with animations and annotations"""
        
        print("Creating visual educational video with animations...")
        
        # Create animated video clips for each step
        clips = []
        
        # 1. Animated introduction
        print("Creating animated introduction...")
        intro_clip = self._create_animated_intro(problem_info)
        clips.append(intro_clip)
        
        # 2. Problem presentation with visual emphasis
        print("Creating problem visualization...")
        problem_clip = self._create_animated_problem(problem_info)
        clips.append(problem_clip)
        
        # 3. Animated solution steps
        print("Creating animated solution steps...")
        for i, step in enumerate(solution.get('steps', []), 1):
            print(f"Creating animated step {i}...")
            step_clip = self._create_animated_step(step, i, len(solution.get('steps', [])))
            clips.append(step_clip)
        
        # 4. Animated conclusion
        print("Creating animated conclusion...")
        conclusion_clip = self._create_animated_conclusion(solution)
        clips.append(conclusion_clip)
        
        # Concatenate all clips (no audio for speed)
        print("Combining animated clips...")
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Generate output filename
        output_filename = f"math_solution_{problem_info.get('problem_type', 'general')}.mp4"
        output_path = os.path.join(self.config.OUTPUT_FOLDER, output_filename)
        
        # Write video file with optimized settings for speed
        print("Rendering video (optimized for speed)...")
        final_video.write_videofile(
            output_path,
            fps=24,  # Lower FPS for faster rendering
            codec='libx264',
            preset='ultrafast',  # Fastest encoding preset
            crf=23,  # Good quality/speed balance
            verbose=False,
            logger=None,
            write_logfile=False,
            threads=4  # Use multiple threads
        )
        
        print(f"Fast video created: {output_path}")
        return output_filename
    
    def _create_animated_intro(self, problem_info: Dict[str, Any]) -> VideoClip:
        """Create animated introduction with visual effects"""
        
        def make_frame(t):
            img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Animated background gradient
            for y in range(self.config.VIDEO_HEIGHT):
                color_intensity = int(255 * (1 - (y / self.config.VIDEO_HEIGHT) * 0.3))
                color = (color_intensity, color_intensity + 20, 255)
                draw.line([(0, y), (self.config.VIDEO_WIDTH, y)], fill=color)
            
            # Animated title with fade-in effect
            title_alpha = min(1.0, t * 2)  # Fade in over 0.5 seconds
            title_color = (int(50 * title_alpha), int(100 * title_alpha), int(200 * title_alpha))
            
            # Title with animation
            title = "🧮 AI Math Problem Solver"
            font_size = 60
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), title, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Animated position (slides in from top)
            y_offset = max(0, 200 - int(t * 100))
            draw.text(((self.config.VIDEO_WIDTH - text_width) // 2, y_offset), 
                     title, fill=title_color, font=font)
            
            # Animated subtitle
            if t > 0.5:
                subtitle_alpha = min(1.0, (t - 0.5) * 2)
                subtitle_color = (int(100 * subtitle_alpha), int(150 * subtitle_alpha), int(200 * subtitle_alpha))
                subtitle = f"Solving {problem_info.get('problem_type', 'mathematical')} problems step by step"
                
                try:
                    subtitle_font = ImageFont.truetype("arial.ttf", 30)
                except:
                    subtitle_font = ImageFont.load_default()
                
                bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
                subtitle_width = bbox[2] - bbox[0]
                draw.text(((self.config.VIDEO_WIDTH - subtitle_width) // 2, y_offset + text_height + 20), 
                         subtitle, fill=subtitle_color, font=subtitle_font)
            
            # Animated mathematical symbols
            if t > 1.0:
                symbols = ["∫", "∑", "π", "√", "α", "β", "γ"]
                for i, symbol in enumerate(symbols):
                    x = 100 + i * 200
                    y = 400 + int(50 * np.sin(t * 3 + i))
                    symbol_color = (int(200 * (0.5 + 0.5 * np.sin(t + i))), 
                                   int(200 * (0.5 + 0.5 * np.cos(t + i))), 
                                   255)
                    
                    try:
                        symbol_font = ImageFont.truetype("arial.ttf", 40)
                    except:
                        symbol_font = ImageFont.load_default()
                    
                    draw.text((x, y), symbol, fill=symbol_color, font=symbol_font)
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=3)
    
    def _create_animated_problem(self, problem_info: Dict[str, Any]) -> VideoClip:
        """Create animated problem presentation with highlighting"""
        
        def make_frame(t):
            img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Background
            for y in range(self.config.VIDEO_HEIGHT):
                color_intensity = int(255 * (1 - (y / self.config.VIDEO_HEIGHT) * 0.2))
                color = (color_intensity, color_intensity + 30, 255)
                draw.line([(0, y), (self.config.VIDEO_WIDTH, y)], fill=color)
            
            # Animated title
            title_alpha = min(1.0, t * 3)
            title_color = (int(50 * title_alpha), int(100 * title_alpha), int(200 * title_alpha))
            
            title = "📝 Problem to Solve:"
            try:
                font = ImageFont.truetype("arial.ttf", 50)
            except:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), title, font=font)
            text_width = bbox[2] - bbox[0]
            draw.text(((self.config.VIDEO_WIDTH - text_width) // 2, 100), 
                     title, fill=title_color, font=font)
            
            # Animated problem text with highlighting
            if t > 0.5:
                problem_text = problem_info.get('original_text', 'No problem provided')
                
                # Create highlighted background
                highlight_y = 200
                highlight_height = 100
                highlight_alpha = min(1.0, (t - 0.5) * 2)
                highlight_color = (int(255 * highlight_alpha), int(255 * highlight_alpha), 
                                 int(200 * highlight_alpha))
                draw.rectangle([50, highlight_y, self.config.VIDEO_WIDTH - 50, 
                              highlight_y + highlight_height], fill=highlight_color, outline=(0, 0, 255), width=3)
                
                # Problem text with typewriter effect
                try:
                    problem_font = ImageFont.truetype("arial.ttf", 36)
                except:
                    problem_font = ImageFont.load_default()
                
                chars_to_show = int((t - 0.5) * len(problem_text) * 2)
                visible_text = problem_text[:chars_to_show]
                
                bbox = draw.textbbox((0, 0), visible_text, font=problem_font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                draw.text(((self.config.VIDEO_WIDTH - text_width) // 2, 
                          highlight_y + (highlight_height - text_height) // 2), 
                         visible_text, fill=(0, 0, 0), font=problem_font)
                
                # Animated cursor
                if chars_to_show < len(problem_text) and int(t * 4) % 2:
                    cursor_x = (self.config.VIDEO_WIDTH - text_width) // 2 + text_width
                    draw.line([(cursor_x, highlight_y + 10), (cursor_x, highlight_y + 90)], 
                             fill=(0, 0, 0), width=3)
            
            # Problem type indicator with animation
            if t > 1.5:
                problem_type = problem_info.get('problem_type', 'general')
                type_alpha = min(1.0, (t - 1.5) * 2)
                type_color = (int(200 * type_alpha), int(100 * type_alpha), int(50 * type_alpha))
                
                type_text = f"Type: {problem_type.title()}"
                try:
                    type_font = ImageFont.truetype("arial.ttf", 24)
                except:
                    type_font = ImageFont.load_default()
                
                bbox = draw.textbbox((0, 0), type_text, font=type_font)
                type_width = bbox[2] - bbox[0]
                draw.text(((self.config.VIDEO_WIDTH - type_width) // 2, 350), 
                         type_text, fill=type_color, font=type_font)
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=4)
    
    def _create_animated_step(self, step: Dict[str, Any], step_number: int, total_steps: int) -> VideoClip:
        """Create animated step with visual transitions and highlighting"""
        
        def make_frame(t):
            img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Animated background
            for y in range(self.config.VIDEO_HEIGHT):
                color_intensity = int(255 * (1 - (y / self.config.VIDEO_HEIGHT) * 0.1))
                color = (color_intensity, color_intensity + 40, 255)
                draw.line([(0, y), (self.config.VIDEO_WIDTH, y)], fill=color)
            
            # Step header with animation
            header_alpha = min(1.0, t * 4)
            header_color = (int(100 * header_alpha), int(200 * header_alpha), int(100 * header_alpha))
            
            step_title = f"Step {step_number} of {total_steps}"
            try:
                header_font = ImageFont.truetype("arial.ttf", 40)
            except:
                header_font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), step_title, font=header_font)
            text_width = bbox[2] - bbox[0]
            
            # Animated slide-in effect
            slide_x = max(0, 100 - int(t * 200))
            draw.text((slide_x, 50), step_title, fill=header_color, font=header_font)
            
            # Progress bar
            progress = step_number / total_steps
            progress_width = int((self.config.VIDEO_WIDTH - 100) * progress * min(1.0, t * 2))
            draw.rectangle([50, 100, 50 + progress_width, 120], fill=(0, 200, 0), outline=(0, 150, 0), width=2)
            draw.rectangle([50, 100, self.config.VIDEO_WIDTH - 50, 120], outline=(0, 150, 0), width=2)
            
            # Step description with fade-in
            if t > 0.3:
                description = step.get('description', '')
                desc_alpha = min(1.0, (t - 0.3) * 2)
                desc_color = (int(50 * desc_alpha), int(50 * desc_alpha), int(200 * desc_alpha))
                
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
                
                # Draw lines with animation
                for i, line in enumerate(lines[:3]):  # Limit to 3 lines
                    y_pos = 150 + i * 35
                    draw.text((60, y_pos), line, fill=desc_color, font=desc_font)
            
            # Step explanation with highlighting
            if t > 0.8:
                explanation = step.get('explanation', '')
                exp_alpha = min(1.0, (t - 0.8) * 1.5)
                exp_color = (int(100 * exp_alpha), int(100 * exp_alpha), int(100 * exp_alpha))
                
                try:
                    exp_font = ImageFont.truetype("arial.ttf", 22)
                except:
                    exp_font = ImageFont.load_default()
                
                # Wrap explanation text
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
                
                # Draw explanation with highlighting background
                for i, line in enumerate(lines[:4]):  # Limit to 4 lines
                    y_pos = 280 + i * 30
                    
                    # Highlight background
                    bbox = draw.textbbox((0, 0), line, font=exp_font)
                    line_width = bbox[2] - bbox[0]
                    highlight_alpha = int(100 * exp_alpha)
                    draw.rectangle([55, y_pos - 5, 55 + line_width + 10, y_pos + 25], 
                                 fill=(highlight_alpha, highlight_alpha, 255))
                    
                    draw.text((60, y_pos), line, fill=(0, 0, 0), font=exp_font)
            
            # Animated mathematical symbols
            if t > 1.2:
                symbols = ["→", "=", "+", "-", "×", "÷", "√"]
                for i, symbol in enumerate(symbols):
                    x = 100 + i * 150
                    y = 450 + int(30 * np.sin(t * 4 + i))
                    symbol_alpha = int(150 * (0.7 + 0.3 * np.sin(t * 2 + i)))
                    symbol_color = (symbol_alpha, symbol_alpha, 255)
                    
                    try:
                        symbol_font = ImageFont.truetype("arial.ttf", 30)
                    except:
                        symbol_font = ImageFont.load_default()
                    
                    draw.text((x, y), symbol, fill=symbol_color, font=symbol_font)
            
            return np.array(img)
        
        duration = max(2, len(step.get('explanation', '')) // 30)  # Adjust based on content
        return VideoClip(make_frame, duration=duration)
    
    def _create_animated_conclusion(self, solution: Dict[str, Any]) -> VideoClip:
        """Create animated conclusion with visual celebration"""
        
        def make_frame(t):
            img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Animated celebration background
            for y in range(self.config.VIDEO_HEIGHT):
                color_intensity = int(255 * (1 - (y / self.config.VIDEO_HEIGHT) * 0.3))
                color = (color_intensity, int(255 * (0.8 + 0.2 * np.sin(t * 2))), 
                        int(255 * (0.6 + 0.4 * np.cos(t * 2))))
                draw.line([(0, y), (self.config.VIDEO_WIDTH, y)], fill=color)
            
            # Animated success title
            title_alpha = min(1.0, t * 3)
            title_scale = 1 + 0.2 * np.sin(t * 6)  # Pulsing effect
            title_color = (int(100 * title_alpha), int(255 * title_alpha), int(100 * title_alpha))
            
            title = "🎉 Solution Complete!"
            try:
                font_size = int(50 * title_scale)
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), title, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Animated position (bounce effect)
            bounce_y = 150 + int(20 * np.sin(t * 8))
            draw.text(((self.config.VIDEO_WIDTH - text_width) // 2, bounce_y), 
                     title, fill=title_color, font=font)
            
            # Final answer with highlighting
            if t > 0.5:
                final_answer = solution.get('final_answer', 'No answer available')
                answer_alpha = min(1.0, (t - 0.5) * 2)
                
                answer_text = f"Final Answer: {final_answer}"
                try:
                    answer_font = ImageFont.truetype("arial.ttf", 36)
                except:
                    answer_font = ImageFont.load_default()
                
                bbox = draw.textbbox((0, 0), answer_text, font=answer_font)
                answer_width = bbox[2] - bbox[0]
                answer_height = bbox[3] - bbox[1]
                
                # Highlighted background
                highlight_alpha = int(255 * answer_alpha)
                draw.rectangle([(self.config.VIDEO_WIDTH - answer_width) // 2 - 20, 
                              bounce_y + text_height + 30 - 10,
                              (self.config.VIDEO_WIDTH - answer_width) // 2 + answer_width + 20,
                              bounce_y + text_height + 30 + answer_height + 10], 
                             fill=(highlight_alpha, highlight_alpha, 255), 
                             outline=(0, 200, 0), width=4)
                
                answer_color = (0, 0, 0)
                draw.text(((self.config.VIDEO_WIDTH - answer_width) // 2, 
                          bounce_y + text_height + 30), 
                         answer_text, fill=answer_color, font=answer_font)
            
            # Animated celebration symbols
            if t > 1.0:
                symbols = ["✨", "🎯", "✅", "🏆", "⭐", "💡", "🎊"]
                for i, symbol in enumerate(symbols):
                    x = 100 + i * 200
                    y = 350 + int(40 * np.sin(t * 3 + i))
                    symbol_alpha = int(200 * (0.6 + 0.4 * np.sin(t * 4 + i)))
                    symbol_color = (symbol_alpha, symbol_alpha, 255)
                    
                    try:
                        symbol_font = ImageFont.truetype("arial.ttf", 35)
                    except:
                        symbol_font = ImageFont.load_default()
                    
                    draw.text((x, y), symbol, fill=symbol_color, font=symbol_font)
            
            # Encouragement message
            if t > 1.5:
                message_alpha = min(1.0, (t - 1.5) * 2)
                message_color = (int(150 * message_alpha), int(150 * message_alpha), int(100 * message_alpha))
                
                message = "Keep practicing mathematics! 🚀"
                try:
                    message_font = ImageFont.truetype("arial.ttf", 24)
                except:
                    message_font = ImageFont.load_default()
                
                bbox = draw.textbbox((0, 0), message, font=message_font)
                message_width = bbox[2] - bbox[0]
                draw.text(((self.config.VIDEO_WIDTH - message_width) // 2, 450), 
                         message, fill=message_color, font=message_font)
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=4)
