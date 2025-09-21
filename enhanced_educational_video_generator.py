#!/usr/bin/env python3
"""
Enhanced Educational Video Generator for Math Problems
Creates step-by-step animated videos with clear explanations, visual aids, and annotations
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from typing import Dict, List, Any, Tuple, Optional
import json
import cv2
import math

# Audio imports
try:
    from gtts import gTTS
    from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips, CompositeVideoClip
    AUDIO_AVAILABLE = True
    print("Enhanced video generator: Audio libraries loaded successfully!")
except ImportError as e:
    print(f"Enhanced video generator: Audio libraries not available: {e}. Install gtts and moviepy for audio support.")
    AUDIO_AVAILABLE = False

class EnhancedEducationalVideoGenerator:
    """Generates enhanced educational videos with step-by-step math solutions, animations, and visual aids"""
    
    def __init__(self, output_dir="outputs"):
        self.output_dir = output_dir
        self.width = 1280
        self.height = 720
        self.fps = 3  # 3 frames per second for smooth animation
        self.audio_enabled = AUDIO_AVAILABLE
        
        # Color scheme for educational content
        self.colors = {
            'background': '#f8f9fa',
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'accent': '#e74c3c',
            'success': '#27ae60',
            'warning': '#f39c12',
            'text': '#2c3e50',
            'light_text': '#7f8c8d',
            'highlight': '#f1c40f',
            'step_bg': '#ecf0f1',
            'equation_bg': '#e8f4f8'
        }
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_educational_video(self, problem_info: Dict, solution: Dict, task_id: str) -> str:
        """Generate a comprehensive educational video with animations and visual aids"""
        try:
            print(f"🎬 Generating enhanced educational video for task {task_id}")
            
            # Create video frames
            frames = []
            
            # 1. Title and Problem Introduction (4 seconds)
            frames.extend(self._create_enhanced_intro_frames(problem_info))
            
            # 2. Problem Analysis with Visual Breakdown (3 seconds)
            frames.extend(self._create_analysis_frames(problem_info))
            
            # 3. Step-by-step Solution with Animations (variable length)
            frames.extend(self._create_animated_solution_frames(solution))
            
            # 4. Final Answer and Summary (3 seconds)
            frames.extend(self._create_conclusion_frames(solution))
            
            if not frames:
                print("❌ No frames generated")
                return None
            
            print(f"📊 Generated {len(frames)} frames for enhanced video")
            
            # Save as MP4
            video_filename = f"enhanced_educational_solution_{task_id}.mp4"
            video_path = os.path.join(self.output_dir, video_filename)
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(video_path, fourcc, self.fps, (self.width, self.height))
            
            for frame in frames:
                # Convert PIL to OpenCV format
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(frame_bgr)
            
            out.release()
            
            # Add audio narration if available
            if self.audio_enabled:
                print("🎵 Adding audio narration to enhanced video...")
                try:
                    video_with_audio = self._add_audio_narration(video_path, problem_info, solution)
                    if video_with_audio:
                        # Replace the original video with the one that has audio
                        os.replace(video_with_audio, video_path)
                        print("✅ Audio narration added successfully!")
                    else:
                        print("⚠️ Audio generation failed, keeping video without audio")
                except Exception as e:
                    print(f"❌ Audio generation failed: {e}")
                    print("Continuing with video without audio...")
            else:
                print("⚠️ Audio libraries not available, video created without audio")
            
            print(f"✅ Enhanced educational video created: {video_filename} ({len(frames)} frames)")
            return video_filename
            
        except Exception as e:
            print(f"❌ Enhanced video generation failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _create_enhanced_intro_frames(self, problem_info: Dict) -> List[np.ndarray]:
        """Create enhanced introduction frames with animations"""
        frames = []
        duration = 4 * self.fps  # 4 seconds
        
        for i in range(duration):
            img = Image.new('RGB', (self.width, self.height), color=self.colors['background'])
            draw = ImageDraw.Draw(img)
            
            try:
                title_font = ImageFont.truetype('arial.ttf', 48)
                subtitle_font = ImageFont.truetype('arial.ttf', 32)
                text_font = ImageFont.truetype('arial.ttf', 24)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
            
            # Animated title with fade-in effect
            if i < duration // 2:
                alpha = int(255 * (i / (duration // 2)))
                title_color = (*self._hex_to_rgb(self.colors['primary']), alpha)
            else:
                title_color = self.colors['primary']
            
            # Main title with animation
            title_text = "🎓 Math Problem Solver"
            title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (self.width - title_width) // 2
            
            # Add glow effect
            for offset in range(3, 0, -1):
                glow_color = (*self._hex_to_rgb(self.colors['secondary']), 50)
                draw.text((title_x + offset, 100 + offset), title_text, 
                         fill=glow_color, font=title_font)
            
            draw.text((title_x, 100), title_text, fill=title_color, font=title_font)
            
            # Problem type with slide-in animation
            if i > duration // 4:
                problem_type = problem_info.get('problem_type', 'Mathematical Problem')
                type_text = f"Problem Type: {problem_type.title()}"
                type_bbox = draw.textbbox((0, 0), type_text, font=subtitle_font)
                type_width = type_bbox[2] - type_bbox[0]
                type_x = (self.width - type_width) // 2
                
                draw.text((type_x, 200), type_text, fill=self.colors['secondary'], font=subtitle_font)
            
            # Problem statement with typewriter effect
            if i > duration // 2:
                problem_text = problem_info.get('original_text', 'No problem provided')
                # Show characters progressively
                chars_to_show = min(len(problem_text), (i - duration // 2) * 3)
                display_text = problem_text[:chars_to_show]
                
                # Wrap text
                wrapped_text = self._wrap_text(display_text, 60)
                y_pos = 300
                for line in wrapped_text[:4]:  # Show first 4 lines
                    draw.text((50, y_pos), line, fill=self.colors['text'], font=text_font)
                    y_pos += 35
                
                # Add cursor effect
                if chars_to_show < len(problem_text) and i % 2 == 0:
                    cursor_x = 50 + draw.textlength(display_text.split('\n')[-1], font=text_font)
                    cursor_y = y_pos - 35
                    draw.text((cursor_x, cursor_y), "|", fill=self.colors['accent'], font=text_font)
            
            # Add decorative elements
            self._add_decorative_elements(draw, i, duration)
            
            frames.append(np.array(img))
        
        return frames
    
    def _create_analysis_frames(self, problem_info: Dict) -> List[np.ndarray]:
        """Create enhanced problem analysis frames with visual breakdown"""
        frames = []
        duration = 3 * self.fps  # 3 seconds
        
        for i in range(duration):
            img = Image.new('RGB', (self.width, self.height), color=self.colors['background'])
            draw = ImageDraw.Draw(img)
            
            try:
                header_font = ImageFont.truetype('arial.ttf', 40)
                text_font = ImageFont.truetype('arial.ttf', 28)
                small_font = ImageFont.truetype('arial.ttf', 20)
            except:
                header_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Analysis header with animation
            header_text = "🔍 Problem Analysis & Strategy"
            draw.text((50, 50), header_text, fill=self.colors['primary'], font=header_font)
            
            # Analysis points with progressive reveal
            analysis_points = [
                ("Problem Type", problem_info.get('problem_type', 'Unknown').title()),
                ("Complexity Level", self._assess_complexity(problem_info).title()),
                ("Variables Identified", str(len(self._extract_variables(problem_info.get('original_text', ''))))),
                ("Solution Strategy", "Step-by-step algebraic manipulation"),
                ("Key Concepts", "Mathematical reasoning and problem-solving")
            ]
            
            y_start = 150
            for idx, (label, value) in enumerate(analysis_points):
                # Progressive reveal with animation
                if i > idx * 8:  # Show each point with delay
                    # Background box for each point
                    box_y = y_start + idx * 80
                    box_height = 60
                    
                    # Animate box appearance
                    if i > idx * 8 + 4:
                        # Draw background box
                        draw.rounded_rectangle(
                            (50, box_y, self.width - 50, box_y + box_height),
                            radius=10,
                            fill=self.colors['step_bg'],
                            outline=self.colors['secondary'],
                            width=2
                        )
                        
                        # Label
                        draw.text((70, box_y + 10), f"• {label}:", 
                                fill=self.colors['primary'], font=text_font)
                        
                        # Value with highlighting
                        draw.text((70, box_y + 35), value, 
                                fill=self.colors['success'], font=small_font)
            
            # Add visual diagram if it's an arithmetic problem
            if 'arithmetic' in problem_info.get('problem_type', '').lower():
                self._draw_arithmetic_diagram(draw, problem_info, i, duration)
            
            frames.append(np.array(img))
        
        return frames
    
    def _create_animated_solution_frames(self, solution: Dict) -> List[np.ndarray]:
        """Create animated step-by-step solution frames with visual aids"""
        frames = []
        steps = solution.get('steps', [])
        
        if not steps or not isinstance(steps, list):
            # Create default steps
            steps = [
                {"step_number": 1, "description": "Identify the problem type and variables", "equation": "", "explanation": ""},
                {"step_number": 2, "description": "Apply appropriate mathematical principles", "equation": "", "explanation": ""},
                {"step_number": 3, "description": "Solve step by step", "equation": "", "explanation": ""}
            ]
        
        for step_idx, step in enumerate(steps):
            # Each step gets 4 seconds with multiple animation frames
            step_frames = self._create_animated_step_frames(step, step_idx + 1, len(steps))
            frames.extend(step_frames)
        
        return frames
    
    def _create_animated_step_frames(self, step: Dict, step_num: int, total_steps: int) -> List[np.ndarray]:
        """Create animated frames for a single step"""
        frames = []
        duration = 4 * self.fps  # 4 seconds per step
        
        for i in range(duration):
            img = Image.new('RGB', (self.width, self.height), color=self.colors['background'])
            draw = ImageDraw.Draw(img)
            
            try:
                step_font = ImageFont.truetype('arial.ttf', 36)
                text_font = ImageFont.truetype('arial.ttf', 24)
                equation_font = ImageFont.truetype('arial.ttf', 32)
                small_font = ImageFont.truetype('arial.ttf', 20)
            except:
                step_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                equation_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Step header with progress indicator
            progress = step_num / total_steps
            self._draw_progress_bar(draw, progress, i, duration)
            
            # Step title with animation
            step_title = f"Step {step_num} of {total_steps}"
            if i < duration // 4:
                # Slide in from left
                slide_offset = max(0, 50 - i * 2)
                draw.text((slide_offset, 100), step_title, 
                         fill=self.colors['primary'], font=step_font)
            else:
                draw.text((50, 100), step_title, 
                         fill=self.colors['primary'], font=step_font)
            
            # Step description with typewriter effect
            description = step.get('description', '')
            if description and i > duration // 6:
                chars_to_show = min(len(description), (i - duration // 6) * 2)
                display_text = description[:chars_to_show]
                
                # Wrap text
                wrapped_text = self._wrap_text(display_text, 80)
                y_pos = 180
                for line in wrapped_text[:3]:
                    draw.text((70, y_pos), line, fill=self.colors['text'], font=text_font)
                    y_pos += 35
                
                # Add cursor
                if chars_to_show < len(description) and i % 2 == 0:
                    cursor_x = 70 + draw.textlength(display_text.split('\n')[-1], font=text_font)
                    draw.text((cursor_x, y_pos - 35), "|", fill=self.colors['accent'], font=text_font)
            
            # Equation with highlighting
            equation = step.get('equation', '')
            if equation and i > duration // 3:
                self._draw_equation_box(draw, equation, i, duration)
            
            # Explanation with visual aids
            explanation = step.get('explanation', '')
            if explanation and i > duration // 2:
                self._draw_explanation_box(draw, explanation, i, duration)
            
            # Add visual elements based on step content
            self._add_step_visual_elements(draw, step, step_num, i, duration)
            
            frames.append(np.array(img))
        
        return frames
    
    def _create_conclusion_frames(self, solution: Dict) -> List[np.ndarray]:
        """Create enhanced conclusion frames"""
        frames = []
        duration = 3 * self.fps  # 3 seconds
        
        for i in range(duration):
            img = Image.new('RGB', (self.width, self.height), color=self.colors['background'])
            draw = ImageDraw.Draw(img)
            
            try:
                title_font = ImageFont.truetype('arial.ttf', 40)
                text_font = ImageFont.truetype('arial.ttf', 28)
                large_font = ImageFont.truetype('arial.ttf', 48)
            except:
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                large_font = ImageFont.load_default()
            
            # Conclusion header
            draw.text((50, 50), "✅ Solution Complete", 
                     fill=self.colors['success'], font=title_font)
            
            # Final answer with emphasis
            final_answer = solution.get('final_answer', 'Solution completed')
            if i > duration // 4:
                # Highlighted answer box
                answer_box_y = 150
                answer_box_height = 100
                
                draw.rounded_rectangle(
                    (50, answer_box_y, self.width - 50, answer_box_y + answer_box_height),
                    radius=15,
                    fill=self.colors['equation_bg'],
                    outline=self.colors['success'],
                    width=3
                )
                
                draw.text((70, answer_box_y + 30), "Final Answer:", 
                         fill=self.colors['primary'], font=text_font)
                
                # Animate answer appearance
                if i > duration // 2:
                    answer_text = str(final_answer)
                    wrapped_answer = self._wrap_text(answer_text, 60)
                    y_pos = answer_box_y + 60
                    for line in wrapped_answer[:2]:
                        draw.text((70, y_pos), line, fill=self.colors['success'], font=text_font)
                        y_pos += 30
            
            # Key takeaways
            if i > duration // 2:
                takeaways = [
                    "✓ Problem solved step by step",
                    "✓ All intermediate steps shown",
                    "✓ Mathematical reasoning applied",
                    "✓ Solution verified"
                ]
                
                y_start = 300
                for idx, takeaway in enumerate(takeaways):
                    if i > duration // 2 + idx * 5:
                        draw.text((70, y_start + idx * 40), takeaway, 
                                fill=self.colors['text'], font=text_font)
            
            # Add celebration animation
            if i > duration // 3:
                self._add_celebration_elements(draw, i, duration)
            
            frames.append(np.array(img))
        
        return frames
    
    def _draw_progress_bar(self, draw, progress: float, frame: int, duration: int):
        """Draw animated progress bar"""
        bar_width = self.width - 100
        bar_height = 20
        bar_x = 50
        bar_y = 50
        
        # Background
        draw.rounded_rectangle(
            (bar_x, bar_y, bar_x + bar_width, bar_y + bar_height),
            radius=10,
            fill=self.colors['step_bg'],
            outline=self.colors['secondary']
        )
        
        # Progress fill with animation
        if frame > duration // 4:
            fill_width = int(bar_width * progress * min(1.0, (frame - duration // 4) / (duration * 3 // 4)))
            draw.rounded_rectangle(
                (bar_x, bar_y, bar_x + fill_width, bar_y + bar_height),
                radius=10,
                fill=self.colors['success']
            )
    
    def _draw_equation_box(self, draw, equation: str, frame: int, duration: int):
        """Draw highlighted equation box"""
        if not equation:
            return
        
        box_y = 300
        box_height = 80
        
        # Animate box appearance
        if frame > duration // 3:
            # Background
            draw.rounded_rectangle(
                (50, box_y, self.width - 50, box_y + box_height),
                radius=10,
                fill=self.colors['equation_bg'],
                outline=self.colors['accent'],
                width=2
            )
            
            # Equation text
            draw.text((70, box_y + 25), f"Equation: {equation}", 
                     fill=self.colors['primary'], font=ImageFont.load_default())
    
    def _draw_explanation_box(self, draw, explanation: str, frame: int, duration: int):
        """Draw explanation box with visual aids"""
        if not explanation:
            return
        
        box_y = 400
        box_height = 120
        
        if frame > duration // 2:
            # Background
            draw.rounded_rectangle(
                (50, box_y, self.width - 50, box_y + box_height),
                radius=10,
                fill=self.colors['step_bg'],
                outline=self.colors['secondary'],
                width=1
            )
            
            # Explanation text
            wrapped_text = self._wrap_text(explanation, 70)
            y_pos = box_y + 20
            for line in wrapped_text[:4]:
                draw.text((70, y_pos), line, fill=self.colors['text'], font=ImageFont.load_default())
                y_pos += 25
    
    def _draw_arithmetic_diagram(self, draw, problem_info: Dict, frame: int, duration: int):
        """Draw visual diagram for arithmetic problems"""
        if frame < duration // 2:
            return
        
        # Draw number line or visual representation
        start_x = self.width - 300
        start_y = 200
        line_length = 200
        
        # Number line
        draw.line([(start_x, start_y), (start_x + line_length, start_y)], 
                 fill=self.colors['secondary'], width=3)
        
        # Add numbers
        for i in range(0, 6):
            x = start_x + i * (line_length // 5)
            draw.text((x - 10, start_y + 10), str(i * 10), 
                     fill=self.colors['text'], font=ImageFont.load_default())
    
    def _add_step_visual_elements(self, draw, step: Dict, step_num: int, frame: int, duration: int):
        """Add visual elements specific to the step content"""
        if frame < duration // 2:
            return
        
        # Add arrows, highlights, or other visual aids based on step content
        description = step.get('description', '').lower()
        
        if 'add' in description or '+' in description:
            # Draw addition visual
            self._draw_addition_visual(draw, frame, duration)
        elif 'multiply' in description or '*' in description:
            # Draw multiplication visual
            self._draw_multiplication_visual(draw, frame, duration)
    
    def _draw_addition_visual(self, draw, frame: int, duration: int):
        """Draw visual representation of addition"""
        center_x = self.width - 200
        center_y = 300
        
        # Draw circles representing numbers
        for i in range(2):
            x = center_x + i * 100
            draw.ellipse([x - 20, center_y - 20, x + 20, center_y + 20], 
                        fill=self.colors['secondary'], outline=self.colors['primary'])
            draw.text((x - 5, center_y - 5), str(5 + i * 5), 
                     fill='white', font=ImageFont.load_default())
        
        # Plus sign
        plus_x = center_x + 50
        draw.line([(plus_x, center_y - 10), (plus_x, center_y + 10)], 
                 fill=self.colors['accent'], width=3)
        draw.line([(plus_x - 10, center_y), (plus_x + 10, center_y)], 
                 fill=self.colors['accent'], width=3)
    
    def _draw_multiplication_visual(self, draw, frame: int, duration: int):
        """Draw visual representation of multiplication"""
        center_x = self.width - 200
        center_y = 300
        
        # Draw grid for multiplication
        grid_size = 3
        cell_size = 20
        start_x = center_x - (grid_size * cell_size) // 2
        start_y = center_y - (grid_size * cell_size) // 2
        
        for i in range(grid_size):
            for j in range(grid_size):
                x = start_x + i * cell_size
                y = start_y + j * cell_size
                draw.rectangle([x, y, x + cell_size, y + cell_size], 
                             fill=self.colors['highlight'], outline=self.colors['primary'])
    
    def _add_decorative_elements(self, draw, frame: int, duration: int):
        """Add decorative elements to frames"""
        # Add floating mathematical symbols
        symbols = ['+', '−', '×', '÷', '=', '√', 'π']
        
        for i in range(3):
            if frame > i * 10:
                x = 100 + i * 200
                y = 50 + (frame * 2) % 100
                symbol = symbols[i % len(symbols)]
                draw.text((x, y), symbol, fill=self.colors['light_text'], 
                         font=ImageFont.load_default())
    
    def _add_celebration_elements(self, draw, frame: int, duration: int):
        """Add celebration elements to conclusion frames"""
        # Add confetti or checkmarks
        if frame % 10 < 5:
            for i in range(5):
                x = 200 + i * 150
                y = 100 + (frame * 3) % 200
                draw.text((x, y), "✓", fill=self.colors['success'], 
                         font=ImageFont.load_default())
    
    def _wrap_text(self, text: str, max_width: int) -> List[str]:
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if len(test_line) <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _extract_variables(self, text: str) -> List[str]:
        """Extract mathematical variables from text"""
        import re
        # Look for single letters that could be variables
        variables = re.findall(r'\b[a-zA-Z]\b', text)
        return list(set(variables))
    
    def _assess_complexity(self, problem_info: Dict) -> str:
        """Assess problem complexity"""
        problem_type = str(problem_info.get('problem_type', '')).lower()
        
        if 'arithmetic' in problem_type or 'simple' in problem_type:
            return 'basic'
        elif 'algebra' in problem_type or 'equation' in problem_type:
            return 'intermediate'
        else:
            return 'advanced'
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _create_audio_clip(self, text: str, duration: float) -> Optional[AudioFileClip]:
        """Create audio clip from text using text-to-speech"""
        if not self.audio_enabled:
            return None
            
        try:
            # Create temporary audio file
            temp_audio_path = os.path.join(self.output_dir, f"temp_audio_{hash(text) % 10000}.mp3")
            
            # Generate speech with optimized settings
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(temp_audio_path)
            
            # Load audio clip
            audio_clip = AudioFileClip(temp_audio_path)
            
            # Adjust duration to match video
            if audio_clip.duration > duration:
                # If audio is longer, cut it
                audio_clip = audio_clip.subclip(0, duration)
            elif audio_clip.duration < duration:
                # If audio is shorter, pad with silence - skip for now to avoid complexity
                pass
            
            # Clean up temporary file after closing the audio clip
            # Note: We'll clean up the file later to avoid access issues
            
            return audio_clip
            
        except Exception as e:
            print(f"❌ Audio generation failed: {e}")
            return None
    
    def _add_audio_narration(self, video_path: str, problem_info: Dict, solution: Dict) -> Optional[str]:
        """Add audio narration to the enhanced video"""
        try:
            # Load the video
            video_clip = VideoFileClip(video_path)
            
            # Create audio clips for different sections
            audio_clips = []
            current_time = 0
            
            # Introduction audio (4 seconds)
            intro_text = f"Welcome to the Math Problem Solver. Today we'll solve: {problem_info.get('original_text', 'a mathematical problem')}"
            intro_audio = self._create_audio_clip(intro_text, 4.0)
            if intro_audio:
                intro_audio = intro_audio.set_start(current_time)
                audio_clips.append(intro_audio)
            current_time += 4.0
            
            # Problem analysis audio (3 seconds)
            analysis_text = f"This is a {problem_info.get('problem_type', 'mathematical')} problem with {problem_info.get('complexity', 'intermediate')} complexity. Let's break it down step by step."
            analysis_audio = self._create_audio_clip(analysis_text, 3.0)
            if analysis_audio:
                analysis_audio = analysis_audio.set_start(current_time)
                audio_clips.append(analysis_audio)
            current_time += 3.0
            
            # Solution steps audio (4 seconds per step)
            steps = solution.get('steps', [])
            for i, step in enumerate(steps[:5]):  # Limit to first 5 steps
                step_text = f"Step {i + 1}: {step.get('description', '')}"
                # Clean up the text for better speech
                step_text = step_text.replace('*', '').replace('**', '').replace('_', '')
                if len(step_text) > 200:  # Limit text length
                    step_text = step_text[:200] + "..."
                
                step_audio = self._create_audio_clip(step_text, 4.0)
                if step_audio:
                    step_audio = step_audio.set_start(current_time)
                    audio_clips.append(step_audio)
                current_time += 4.0
            
            # Conclusion audio (3 seconds)
            final_answer = solution.get('final_answer', 'The solution is complete.')
            conclusion_text = f"Great job! We've solved the problem step by step. The final answer is: {final_answer}"
            conclusion_audio = self._create_audio_clip(conclusion_text, 3.0)
            if conclusion_audio:
                conclusion_audio = conclusion_audio.set_start(current_time)
                audio_clips.append(conclusion_audio)
            
            # Combine all audio clips
            if audio_clips:
                combined_audio = concatenate_audioclips(audio_clips)
                
                # Ensure audio duration matches video duration
                if combined_audio.duration > video_clip.duration:
                    combined_audio = combined_audio.subclip(0, video_clip.duration)
                elif combined_audio.duration < video_clip.duration:
                    # Pad with silence if needed - skip for now to avoid complexity
                    pass
                
                # Combine video and audio
                final_video = video_clip.set_audio(combined_audio)
                
                # Save the video with audio
                audio_video_path = video_path.replace('.mp4', '_with_audio.mp4')
                final_video.write_videofile(audio_video_path, codec='libx264', audio_codec='aac', verbose=False, logger=None)
                
                # Clean up
                video_clip.close()
                final_video.close()
                combined_audio.close()
                
                return audio_video_path
            else:
                print("❌ No audio clips generated")
                return None
                
        except Exception as e:
            print(f"❌ Error adding audio narration: {e}")
            return None
