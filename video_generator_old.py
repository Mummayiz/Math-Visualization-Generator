import os
import tempfile
from typing import Dict, List, Any, Optional
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io
from config import Config

# Import moviepy for video generation
from moviepy.editor import *
MOVIEPY_AVAILABLE = True

# Try to import gTTS, fallback if not available
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("gTTS not available, audio generation will be limited")

class VideoGenerator:
    """Generates educational videos from mathematical solutions"""
    
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
    
    # Legacy methods removed - using new animated methods above
    
    def _create_problem_clip(self, problem_info: Dict[str, Any]) -> VideoClip:
        """Create problem presentation clip"""
        
        def make_frame(t):
            # Create a light blue background
            img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'lightblue')
            draw = ImageDraw.Draw(img)
            
            try:
                title_font = ImageFont.truetype("arial.ttf", 50)
                text_font = ImageFont.truetype("arial.ttf", 36)
            except:
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
            
            # Draw title
            title = "Problem Statement"
            bbox = draw.textbbox((0, 0), title, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (self.config.VIDEO_WIDTH - text_width) // 2
            y = 100
            
            draw.text((x, y), title, fill='darkblue', font=title_font)
            
            # Draw problem text
            problem_text = problem_info.get('original_text', 'No problem text available')
            
            # Wrap text
            lines = self._wrap_text(problem_text, 80)
            y_offset = 200
            
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=text_font)
                text_width = bbox[2] - bbox[0]
                x = (self.config.VIDEO_WIDTH - text_width) // 2
                draw.text((x, y_offset), line, fill='black', font=text_font)
                y_offset += 50
            
            return np.array(img)
        
        # Create video clip
        clip = VideoClip(make_frame, duration=4)
        
        # Add narration
        narration_text = f"Here's the problem we need to solve: {problem_info.get('original_text', '')}"
        audio_clip = self._create_audio_clip(narration_text)
        
        # Ensure audio duration matches video duration
        if audio_clip.duration > clip.duration:
            audio_clip = audio_clip.subclip(0, clip.duration)
        elif audio_clip.duration < clip.duration:
            # Loop audio if it's shorter than video
            loops_needed = int(clip.duration / audio_clip.duration) + 1
            audio_clip = concatenate_audioclips([audio_clip] * loops_needed).subclip(0, clip.duration)
        
        clip = clip.set_audio(audio_clip)
        
        return clip
    
    def _create_step_clip(self, step: Dict[str, Any], step_number: int, total_steps: int) -> VideoClip:
        """Create a clip for a solution step"""
        
        def make_frame(t):
            # Create a white background
            img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            try:
                title_font = ImageFont.truetype("arial.ttf", 45)
                text_font = ImageFont.truetype("arial.ttf", 32)
                equation_font = ImageFont.truetype("arial.ttf", 40)
            except:
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                equation_font = ImageFont.load_default()
            
            # Draw step header
            step_title = f"Step {step_number} of {total_steps}"
            bbox = draw.textbbox((0, 0), step_title, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (self.config.VIDEO_WIDTH - text_width) // 2
            y = 50
            
            draw.text((x, y), step_title, fill='darkgreen', font=title_font)
            
            # Draw step description
            description = step.get('description', '')
            if description:
                lines = self._wrap_text(description, 60)
                y_offset = 150
                
                for line in lines:
                    bbox = draw.textbbox((0, 0), line, font=text_font)
                    text_width = bbox[2] - bbox[0]
                    x = (self.config.VIDEO_WIDTH - text_width) // 2
                    draw.text((x, y_offset), line, fill='black', font=text_font)
                    y_offset += 40
            
            # Draw equation
            equation = step.get('equation', '')
            if equation:
                # Draw equation in a box
                equation_lines = self._wrap_text(equation, 50)
                y_offset = 300
                
                for line in equation_lines:
                    bbox = draw.textbbox((0, 0), line, font=equation_font)
                    text_width = bbox[2] - bbox[0]
                    x = (self.config.VIDEO_WIDTH - text_width) // 2
                    draw.text((x, y_offset), line, fill='darkred', font=equation_font)
                    y_offset += 50
                
                # Draw box around equation
                box_x = 100
                box_y = 280
                box_width = self.config.VIDEO_WIDTH - 200
                box_height = y_offset - 280 + 20
                
                draw.rectangle([box_x, box_y, box_x + box_width, box_y + box_height], 
                             outline='darkred', width=3)
            
            # Draw explanation
            explanation = step.get('explanation', '')
            if explanation:
                lines = self._wrap_text(explanation, 70)
                y_offset = 500
                
                for line in lines:
                    bbox = draw.textbbox((0, 0), line, font=text_font)
                    text_width = bbox[2] - bbox[0]
                    x = (self.config.VIDEO_WIDTH - text_width) // 2
                    draw.text((x, y_offset), line, fill='darkblue', font=text_font)
                    y_offset += 35
            
            return np.array(img)
        
        # Create video clip
        duration = max(3, len(step.get('explanation', '')) // 20)  # Adjust duration based on content
        clip = VideoClip(make_frame, duration=duration)
        
        # Add narration
        narration_text = f"Step {step_number}: {step.get('description', '')}. {step.get('explanation', '')}"
        audio_clip = self._create_audio_clip(narration_text)
        
        # Ensure audio duration matches video duration
        if audio_clip.duration > clip.duration:
            audio_clip = audio_clip.subclip(0, clip.duration)
        elif audio_clip.duration < clip.duration:
            # Loop audio if it's shorter than video
            loops_needed = int(clip.duration / audio_clip.duration) + 1
            audio_clip = concatenate_audioclips([audio_clip] * loops_needed).subclip(0, clip.duration)
        
        clip = clip.set_audio(audio_clip)
        
        return clip
    
    def _create_conclusion_clip(self, solution: Dict[str, Any]) -> VideoClip:
        """Create conclusion clip for the video"""
        
        def make_frame(t):
            # Create a light green background
            img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'lightgreen')
            draw = ImageDraw.Draw(img)
            
            try:
                title_font = ImageFont.truetype("arial.ttf", 50)
                text_font = ImageFont.truetype("arial.ttf", 36)
                answer_font = ImageFont.truetype("arial.ttf", 40)
            except:
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                answer_font = ImageFont.load_default()
            
            # Draw title
            title = "Solution Complete!"
            bbox = draw.textbbox((0, 0), title, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (self.config.VIDEO_WIDTH - text_width) // 2
            y = 100
            
            draw.text((x, y), title, fill='darkgreen', font=title_font)
            
            # Draw final answer
            final_answer = solution.get('final_answer', 'No answer available')
            if final_answer:
                answer_text = f"Final Answer: {final_answer}"
                lines = self._wrap_text(answer_text, 60)
                y_offset = 250
                
                for line in lines:
                    bbox = draw.textbbox((0, 0), line, font=answer_font)
                    text_width = bbox[2] - bbox[0]
                    x = (self.config.VIDEO_WIDTH - text_width) // 2
                    draw.text((x, y_offset), line, fill='darkred', font=answer_font)
                    y_offset += 50
                
                # Draw box around answer
                box_x = 100
                box_y = 220
                box_width = self.config.VIDEO_WIDTH - 200
                box_height = y_offset - 220 + 20
                
                draw.rectangle([box_x, box_y, box_x + box_width, box_y + box_height], 
                             outline='darkred', width=4)
            
            # Draw closing message
            closing_text = "Thank you for watching! Practice makes perfect in mathematics."
            bbox = draw.textbbox((0, 0), closing_text, font=text_font)
            text_width = bbox[2] - bbox[0]
            x = (self.config.VIDEO_WIDTH - text_width) // 2
            y = 500
            
            draw.text((x, y), closing_text, fill='darkblue', font=text_font)
            
            return np.array(img)
        
        # Create video clip
        clip = VideoClip(make_frame, duration=4)
        
        # Add narration
        final_answer = solution.get('final_answer', 'No answer available')
        narration_text = f"Great job! We've completed the solution. The final answer is {final_answer}. Keep practicing mathematics!"
        audio_clip = self._create_audio_clip(narration_text)
        
        # Ensure audio duration matches video duration
        if audio_clip.duration > clip.duration:
            audio_clip = audio_clip.subclip(0, clip.duration)
        elif audio_clip.duration < clip.duration:
            # Loop audio if it's shorter than video
            loops_needed = int(clip.duration / audio_clip.duration) + 1
            audio_clip = concatenate_audioclips([audio_clip] * loops_needed).subclip(0, clip.duration)
        
        clip = clip.set_audio(audio_clip)
        
        return clip
    
    def _create_audio_clip(self, text: str):
        """Create audio clip from text using text-to-speech"""
        if not GTTS_AVAILABLE:
            # Return silent audio if TTS is not available
            return AudioClip(lambda t: 0, duration=3)
            
        try:
            # Use gTTS for text-to-speech
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Create temporary file in the outputs directory
            temp_filename = f"temp_audio_{hash(text) % 10000}.mp3"
            temp_path = os.path.join(self.config.OUTPUT_FOLDER, temp_filename)
            
            # Save audio to file
            tts.save(temp_path)
            
            # Load as audio clip
            audio_clip = AudioFileClip(temp_path)
            
            # Store temp file for cleanup later
            if not hasattr(self, '_temp_files'):
                self._temp_files = []
            self._temp_files.append(temp_path)
            
            return audio_clip
                
        except Exception as e:
            print(f"Error creating audio: {e}")
            # Return silent audio if TTS fails
            return AudioClip(lambda t: 0, duration=3)
    
    def _cleanup_temp_files(self):
        """Clean up temporary audio files"""
        if hasattr(self, '_temp_files'):
            for temp_file in self._temp_files:
                try:
                    if os.path.exists(temp_file):
                        os.unlink(temp_file)
                except Exception as e:
                    print(f"Error cleaning up temp file {temp_file}: {e}")
            self._temp_files = []
    
    def _wrap_text(self, text: str, max_width: int) -> List[str]:
        """Wrap text to fit within specified width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            line_text = ' '.join(current_line)
            
            # Simple character-based wrapping
            if len(line_text) > max_width:
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
    
    def _generate_image_slideshow(self, problem_info: Dict[str, Any], solution: Dict[str, Any]) -> str:
        """Generate an image slideshow when video generation is not available"""
        print("Generating image slideshow instead of video...")
        
        # Create slideshow directory
        slideshow_dir = os.path.join(self.config.OUTPUT_FOLDER, "slideshow")
        os.makedirs(slideshow_dir, exist_ok=True)
        
        slide_count = 0
        
        # 1. Introduction slide
        intro_img = self._create_intro_image(problem_info)
        intro_path = os.path.join(slideshow_dir, f"slide_{slide_count:02d}_intro.png")
        intro_img.save(intro_path)
        slide_count += 1
        
        # 2. Problem slide
        problem_img = self._create_problem_image(problem_info)
        problem_path = os.path.join(slideshow_dir, f"slide_{slide_count:02d}_problem.png")
        problem_img.save(problem_path)
        slide_count += 1
        
        # 3. Solution step slides
        for i, step in enumerate(solution.get('steps', []), 1):
            step_img = self._create_step_image(step, i, len(solution.get('steps', [])))
            step_path = os.path.join(slideshow_dir, f"slide_{slide_count:02d}_step_{i}.png")
            step_img.save(step_path)
            slide_count += 1
        
        # 4. Conclusion slide
        conclusion_img = self._create_conclusion_image(solution)
        conclusion_path = os.path.join(slideshow_dir, f"slide_{slide_count:02d}_conclusion.png")
        conclusion_img.save(conclusion_path)
        slide_count += 1
        
        # Create a simple HTML slideshow
        html_path = self._create_html_slideshow(slideshow_dir, slide_count)
        
        print(f"Image slideshow created in: {slideshow_dir}")
        print(f"HTML slideshow: {html_path}")
        
        # Return just the filename for the download link
        return "slideshow.html"
    
    def _create_intro_image(self, problem_info: Dict[str, Any]) -> Image.Image:
        """Create introduction image"""
        img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'white')
        draw = ImageDraw.Draw(img)
        
        try:
            title_font = ImageFont.truetype("arial.ttf", 60)
            subtitle_font = ImageFont.truetype("arial.ttf", 40)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # Draw title
        title = "Math Problem Solver"
        bbox = draw.textbbox((0, 0), title, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (self.config.VIDEO_WIDTH - text_width) // 2
        y = 200
        draw.text((x, y), title, fill='darkblue', font=title_font)
        
        # Draw subtitle
        subtitle = f"{problem_info.get('problem_type', 'General').title()} Problem"
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        x = (self.config.VIDEO_WIDTH - text_width) // 2
        y += 100
        draw.text((x, y), subtitle, fill='blue', font=subtitle_font)
        
        return img
    
    def _create_problem_image(self, problem_info: Dict[str, Any]) -> Image.Image:
        """Create problem image"""
        img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'lightblue')
        draw = ImageDraw.Draw(img)
        
        try:
            title_font = ImageFont.truetype("arial.ttf", 50)
            text_font = ImageFont.truetype("arial.ttf", 36)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
        
        # Draw title
        title = "Problem Statement"
        bbox = draw.textbbox((0, 0), title, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (self.config.VIDEO_WIDTH - text_width) // 2
        y = 100
        draw.text((x, y), title, fill='darkblue', font=title_font)
        
        # Draw problem text
        problem_text = problem_info.get('original_text', 'No problem text available')
        lines = self._wrap_text(problem_text, 80)
        y_offset = 200
        
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=text_font)
            text_width = bbox[2] - bbox[0]
            x = (self.config.VIDEO_WIDTH - text_width) // 2
            draw.text((x, y_offset), line, fill='black', font=text_font)
            y_offset += 50
        
        return img
    
    def _create_step_image(self, step: Dict[str, Any], step_number: int, total_steps: int) -> Image.Image:
        """Create step image"""
        img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'white')
        draw = ImageDraw.Draw(img)
        
        try:
            title_font = ImageFont.truetype("arial.ttf", 45)
            text_font = ImageFont.truetype("arial.ttf", 32)
            equation_font = ImageFont.truetype("arial.ttf", 40)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            equation_font = ImageFont.load_default()
        
        # Draw step header
        step_title = f"Step {step_number} of {total_steps}"
        bbox = draw.textbbox((0, 0), step_title, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (self.config.VIDEO_WIDTH - text_width) // 2
        y = 50
        draw.text((x, y), step_title, fill='darkgreen', font=title_font)
        
        # Draw step description
        description = step.get('description', '')
        if description:
            lines = self._wrap_text(description, 60)
            y_offset = 150
            
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=text_font)
                text_width = bbox[2] - bbox[0]
                x = (self.config.VIDEO_WIDTH - text_width) // 2
                draw.text((x, y_offset), line, fill='black', font=text_font)
                y_offset += 40
        
        # Draw equation
        equation = step.get('equation', '')
        if equation:
            lines = self._wrap_text(equation, 50)
            y_offset = 300
            
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=equation_font)
                text_width = bbox[2] - bbox[0]
                x = (self.config.VIDEO_WIDTH - text_width) // 2
                draw.text((x, y_offset), line, fill='darkred', font=equation_font)
                y_offset += 50
        
        # Draw explanation
        explanation = step.get('explanation', '')
        if explanation:
            lines = self._wrap_text(explanation, 70)
            y_offset = 500
            
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=text_font)
                text_width = bbox[2] - bbox[0]
                x = (self.config.VIDEO_WIDTH - text_width) // 2
                draw.text((x, y_offset), line, fill='darkblue', font=text_font)
                y_offset += 35
        
        return img
    
    def _create_conclusion_image(self, solution: Dict[str, Any]) -> Image.Image:
        """Create conclusion image"""
        img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'lightgreen')
        draw = ImageDraw.Draw(img)
        
        try:
            title_font = ImageFont.truetype("arial.ttf", 50)
            text_font = ImageFont.truetype("arial.ttf", 36)
            answer_font = ImageFont.truetype("arial.ttf", 40)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            answer_font = ImageFont.load_default()
        
        # Draw title
        title = "Solution Complete!"
        bbox = draw.textbbox((0, 0), title, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (self.config.VIDEO_WIDTH - text_width) // 2
        y = 100
        draw.text((x, y), title, fill='darkgreen', font=title_font)
        
        # Draw final answer
        final_answer = solution.get('final_answer', 'No answer available')
        if final_answer:
            answer_text = f"Final Answer: {final_answer}"
            lines = self._wrap_text(answer_text, 60)
            y_offset = 250
            
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=answer_font)
                text_width = bbox[2] - bbox[0]
                x = (self.config.VIDEO_WIDTH - text_width) // 2
                draw.text((x, y_offset), line, fill='darkred', font=answer_font)
                y_offset += 50
        
        return img
    
    def _create_html_slideshow(self, slideshow_dir: str, slide_count: int) -> str:
        """Create HTML slideshow"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Math Solution Slideshow</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .slideshow-container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .slide {{
            display: none;
            text-align: center;
            padding: 20px;
        }}
        .slide.active {{
            display: block;
        }}
        .slide img {{
            max-width: 100%;
            height: auto;
            border-radius: 5px;
        }}
        .controls {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
        }}
        .btn {{
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 0 10px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }}
        .btn:hover {{
            background: #0056b3;
        }}
        .slide-counter {{
            margin: 10px 0;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="slideshow-container">
        <div class="slide active">
            <img src="slide_00_intro.png" alt="Introduction">
        </div>
        <div class="slide">
            <img src="slide_01_problem.png" alt="Problem">
        </div>
"""
        
        # Add step slides
        for i in range(2, slide_count - 1):
            html_content += f"""
        <div class="slide">
            <img src="slide_{i:02d}_step_{i-1}.png" alt="Step {i-1}">
        </div>
"""
        
        # Add conclusion slide
        html_content += f"""
        <div class="slide">
            <img src="slide_{slide_count-1:02d}_conclusion.png" alt="Conclusion">
        </div>
        
        <div class="controls">
            <button class="btn" onclick="previousSlide()">Previous</button>
            <button class="btn" onclick="nextSlide()">Next</button>
            <div class="slide-counter">
                <span id="current">1</span> / <span id="total">{slide_count}</span>
            </div>
        </div>
    </div>

    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        
        function showSlide(n) {{
            slides[currentSlide].classList.remove('active');
            currentSlide = (n + totalSlides) % totalSlides;
            slides[currentSlide].classList.add('active');
            document.getElementById('current').textContent = currentSlide + 1;
        }}
        
        function nextSlide() {{
            showSlide(currentSlide + 1);
        }}
        
        function previousSlide() {{
            showSlide(currentSlide - 1);
        }}
        
        // Auto-advance slides every 5 seconds
        setInterval(nextSlide, 5000);
        
        // Keyboard navigation
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'ArrowRight') nextSlide();
            if (e.key === 'ArrowLeft') previousSlide();
        }});
    </script>
</body>
</html>
"""
        
        html_path = os.path.join(slideshow_dir, "slideshow.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_path
