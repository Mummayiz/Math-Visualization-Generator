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

# Import text-to-speech
try:
    from gtts import gTTS
    AUDIO_AVAILABLE = True
    print("Audio libraries loaded successfully!")
except ImportError as e:
    AUDIO_AVAILABLE = False
    print(f"Audio libraries not available: {e}. Install gtts for audio support.")

class VideoGenerator:
    """Fast and accurate video generator without animations"""
    
    def __init__(self):
        self.config = Config()
        self.ensure_directories()
        self.audio_enabled = AUDIO_AVAILABLE
        
    def ensure_directories(self):
        """Create necessary directories"""
        Config.ensure_directories()
        
    def _create_audio_clip(self, text: str, duration: float) -> Optional[AudioClip]:
        """Create audio clip from text using text-to-speech"""
        if not self.audio_enabled:
            return None
            
        try:
            # Create temporary audio file
            temp_audio_path = os.path.join(self.config.TEMP_FOLDER, f"temp_audio_{hash(text) % 10000}.mp3")
            
            # Generate speech with optimized settings
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(temp_audio_path)
            
            # Load audio clip
            audio_clip = AudioFileClip(temp_audio_path)
            
            # Adjust to match duration exactly
            if audio_clip.duration > duration:
                # If audio is longer, cut it
                audio_clip = audio_clip.subclip(0, duration)
            elif audio_clip.duration < duration:
                # If audio is shorter, pad with silence
                silence_duration = duration - audio_clip.duration
                silence = AudioClip(lambda t: 0, duration=silence_duration)
                audio_clip = concatenate_audioclips([audio_clip, silence])
            
            # Set volume
            audio_clip = audio_clip.volumex(self.config.VOICE_VOLUME)
            
            return audio_clip
            
        except Exception as e:
            print(f"Audio generation failed: {e}")
            return None
        
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
        
        # Add audio narration if available
        if self.audio_enabled:
            print("Adding audio narration...")
            print(f"Video duration: {final_video.duration} seconds")
            try:
                final_video = self._add_audio_narration(final_video, problem_info, solution)
                print(f"Audio narration added successfully! Final video duration: {final_video.duration} seconds")
            except Exception as e:
                print(f"Failed to add audio narration: {e}")
                print("Continuing with video without audio...")
        
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
        
        print(f"Video with audio created: {output_path}")
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
        
        return VideoClip(make_frame, duration=2.0)  # Fixed duration to match audio
    
    def _create_simple_problem(self, problem_info: Dict[str, Any]) -> VideoClip:
        """Create tutor-style problem presentation with analysis"""
        
        def make_frame(t):
            img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), '#F8F9FA')
            draw = ImageDraw.Draw(img)
            
            # Professional header with gradient
            title = "📚 Problem Analysis & Solution Plan"
            try:
                title_font = ImageFont.truetype("arial.ttf", 45)
            except:
                title_font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), title, font=title_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Draw title background with gradient effect
            draw.rectangle([40, 30, self.config.VIDEO_WIDTH - 40, 100], 
                         fill='#2C3E50', outline='#1A252F', width=3)
            
            draw.text(((self.config.VIDEO_WIDTH - text_width) // 2, 65 - text_height//2), 
                     title, fill='white', font=title_font)
            
            y_pos = 120
            
            # Problem type analysis
            problem_type = problem_info.get('problem_type', 'general')
            type_label = f"🎯 Problem Type: {problem_type.title()}"
            try:
                type_font = ImageFont.truetype("arial.ttf", 32)
            except:
                type_font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), type_label, font=type_font)
            line_width = bbox[2] - bbox[0]
            
            draw.rectangle([50, y_pos - 8, 50 + line_width + 20, y_pos + 40], 
                         fill='#E3F2FD', outline='#1976D2', width=2)
            draw.text((70, y_pos), type_label, fill='#0D47A1', font=type_font)
            y_pos += 60
            
            # Problem statement with enhanced formatting
            problem_text = problem_info.get('original_text', 'No problem provided')
            prob_label = "📝 Problem Statement:"
            try:
                prob_label_font = ImageFont.truetype("arial.ttf", 28)
            except:
                prob_label_font = ImageFont.load_default()
            
            draw.text((60, y_pos), prob_label, fill='#D32F2F', font=prob_label_font)
            y_pos += 40
            
            # Problem text with mathematical formatting
            try:
                text_font = ImageFont.truetype("arial.ttf", 36)
            except:
                text_font = ImageFont.load_default()
            
            # Wrap text with better spacing
            words = problem_text.split()
            lines = []
            current_line = []
            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                bbox = draw.textbbox((0, 0), test_line, font=text_font)
                if bbox[2] - bbox[0] > self.config.VIDEO_WIDTH - 120:
                    if len(current_line) > 1:
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
                        current_line = []
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw problem lines with enhanced styling
            for i, line in enumerate(lines[:5]):  # Limit to 5 lines
                bbox = draw.textbbox((0, 0), line, font=text_font)
                line_width = bbox[2] - bbox[0]
                line_height = bbox[3] - bbox[1]
                
                x = (self.config.VIDEO_WIDTH - line_width) // 2
                
                # Enhanced background with mathematical styling
                draw.rectangle([x - 25, y_pos - 12, x + line_width + 25, y_pos + line_height + 12], 
                             fill='white', outline='#FF5722', width=3)
                draw.text((x, y_pos), line, fill='#D84315', font=text_font)
                y_pos += line_height + 25
            
            y_pos += 20
            
            # Solution strategy preview
            strategy_label = "🔍 Solution Strategy:"
            try:
                strategy_font = ImageFont.truetype("arial.ttf", 28)
            except:
                strategy_font = ImageFont.load_default()
            
            draw.text((60, y_pos), strategy_label, fill='#7B1FA2', font=strategy_font)
            y_pos += 40
            
            # Strategy explanation
            strategy_text = self._generate_solution_strategy(problem_type, problem_text)
            try:
                strategy_text_font = ImageFont.truetype("arial.ttf", 26)
            except:
                strategy_text_font = ImageFont.load_default()
            
            # Wrap strategy text
            words = strategy_text.split()
            lines = []
            current_line = []
            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                bbox = draw.textbbox((0, 0), test_line, font=strategy_text_font)
                if bbox[2] - bbox[0] > self.config.VIDEO_WIDTH - 120:
                    if len(current_line) > 1:
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
                        current_line = []
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw strategy lines
            for i, line in enumerate(lines[:3]):  # Limit to 3 lines
                bbox = draw.textbbox((0, 0), line, font=strategy_text_font)
                line_width = bbox[2] - bbox[0]
                line_height = bbox[3] - bbox[1]
                
                draw.rectangle([50, y_pos - 8, 50 + line_width + 20, y_pos + line_height + 8], 
                             fill='#F3E5F5', outline='#8E24AA', width=2)
                draw.text((70, y_pos), line, fill='#4A148C', font=strategy_text_font)
                y_pos += line_height + 20
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=6.0)  # Fixed duration to match audio
    
    def _generate_solution_strategy(self, problem_type: str, problem_text: str) -> str:
        """Generate solution strategy based on problem type"""
        strategies = {
            'algebra': 'We will isolate the variable by performing inverse operations step by step',
            'geometry': 'We will use geometric formulas and properties to find the unknown values',
            'calculus': 'We will apply differentiation or integration techniques to solve the problem',
            'trigonometry': 'We will use trigonometric identities and ratios to find the solution',
            'statistics': 'We will apply statistical formulas and probability concepts',
            'arithmetic': 'We will use basic arithmetic operations to solve the problem',
            'general': 'We will analyze the problem and apply appropriate mathematical methods'
        }
        
        return strategies.get(problem_type.lower(), strategies['general'])
    
    def _create_simple_step(self, step: Dict[str, Any], step_number: int, total_steps: int) -> VideoClip:
        """Create tutor-style step with detailed explanations and key concepts"""
        
        def make_frame(t):
            img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Create a more professional tutor-style layout
            # Step header with progress indicator
            step_title = f"Step {step_number} of {total_steps}"
            try:
                header_font = ImageFont.truetype("arial.ttf", 45)
            except:
                header_font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), step_title, font=header_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Draw header with gradient effect
            draw.rectangle([40, 20, self.config.VIDEO_WIDTH - 40, 90], 
                         fill='#2E86AB', outline='#1B4F72', width=3)
            
            draw.text(((self.config.VIDEO_WIDTH - text_width) // 2, 45 - text_height//2), 
                     step_title, fill='white', font=header_font)
            
            # Progress bar
            progress = step_number / total_steps
            progress_width = int((self.config.VIDEO_WIDTH - 100) * progress)
            draw.rectangle([50, 100, 50 + progress_width, 110], fill='#28A745', outline='#1E7E34', width=2)
            draw.rectangle([50, 100, self.config.VIDEO_WIDTH - 50, 110], outline='#6C757D', width=2)
            
            y_pos = 130
            
            # Key Concept Highlight Box
            key_concept = self._extract_key_concept(step)
            if key_concept:
                # Key concept header
                concept_label = "🎯 Key Concept:"
                try:
                    concept_header_font = ImageFont.truetype("arial.ttf", 28)
                except:
                    concept_header_font = ImageFont.load_default()
                
                draw.text((60, y_pos), concept_label, fill='#DC3545', font=concept_header_font)
                y_pos += 40
                
                # Key concept text with special highlighting
                try:
                    concept_font = ImageFont.truetype("arial.ttf", 32)
                except:
                    concept_font = ImageFont.load_default()
                
                # Draw key concept with special styling
                bbox = draw.textbbox((0, 0), key_concept, font=concept_font)
                line_width = bbox[2] - bbox[0]
                line_height = bbox[3] - bbox[1]
                
                # Special highlight background
                draw.rectangle([50, y_pos - 10, 50 + line_width + 30, y_pos + line_height + 10], 
                             fill='#FFF3CD', outline='#FFC107', width=3)
                draw.text((70, y_pos), key_concept, fill='#856404', font=concept_font)
                y_pos += line_height + 30
            
            # Mathematical Operation/Transformation
            operation = self._extract_operation(step)
            if operation:
                # Operation header
                op_label = "🔢 Mathematical Operation:"
                try:
                    op_header_font = ImageFont.truetype("arial.ttf", 28)
                except:
                    op_header_font = ImageFont.load_default()
                
                draw.text((60, y_pos), op_label, fill='#6F42C1', font=op_header_font)
                y_pos += 40
                
                # Operation text with special formatting
                try:
                    op_font = ImageFont.truetype("arial.ttf", 36)
                except:
                    op_font = ImageFont.load_default()
                
                # Draw operation with mathematical styling
                bbox = draw.textbbox((0, 0), operation, font=op_font)
                line_width = bbox[2] - bbox[0]
                line_height = bbox[3] - bbox[1]
                
                # Mathematical operation background
                draw.rectangle([50, y_pos - 10, 50 + line_width + 30, y_pos + line_height + 10], 
                             fill='#E7F3FF', outline='#007BFF', width=3)
                draw.text((70, y_pos), operation, fill='#004085', font=op_font)
                y_pos += line_height + 30
            
            # Step description with tutor guidance
            description = step.get('description', '')
            if description:
                # Description label
                desc_label = "📝 What we're doing:"
                try:
                    label_font = ImageFont.truetype("arial.ttf", 28)
                except:
                    label_font = ImageFont.load_default()
                
                draw.text((60, y_pos), desc_label, fill='#E83E8C', font=label_font)
                y_pos += 40
                
                # Description text with better formatting
                try:
                    desc_font = ImageFont.truetype("arial.ttf", 30)
                except:
                    desc_font = ImageFont.load_default()
                
                # Wrap text with better spacing
                words = description.split()
                lines = []
                current_line = []
                for word in words:
                    current_line.append(word)
                    test_line = ' '.join(current_line)
                    bbox = draw.textbbox((0, 0), test_line, font=desc_font)
                    if bbox[2] - bbox[0] > self.config.VIDEO_WIDTH - 120:
                        if len(current_line) > 1:
                            current_line.pop()
                            lines.append(' '.join(current_line))
                            current_line = [word]
                        else:
                            lines.append(word)
                            current_line = []
                if current_line:
                    lines.append(' '.join(current_line))
                
                # Draw description lines with background
                for i, line in enumerate(lines[:3]):  # Limit to 3 lines
                    bbox = draw.textbbox((0, 0), line, font=desc_font)
                    line_width = bbox[2] - bbox[0]
                    line_height = bbox[3] - bbox[1]
                    
                    draw.rectangle([50, y_pos - 8, 50 + line_width + 20, y_pos + line_height + 8], 
                                 fill='#FFF8E1', outline='#FF9800', width=2)
                    draw.text((70, y_pos), line, fill='#E65100', font=desc_font)
                    y_pos += line_height + 20
                
                y_pos += 20
            
            # Step explanation with reasoning
            explanation = step.get('explanation', '')
            if explanation:
                # Explanation label
                exp_label = "💡 Why we do this (Reasoning):"
                try:
                    exp_label_font = ImageFont.truetype("arial.ttf", 28)
                except:
                    exp_label_font = ImageFont.load_default()
                
                draw.text((60, y_pos), exp_label, fill='#28A745', font=exp_label_font)
                y_pos += 40
                
                # Explanation text
                try:
                    exp_font = ImageFont.truetype("arial.ttf", 26)
                except:
                    exp_font = ImageFont.load_default()
                
                # Wrap text with better spacing
                words = explanation.split()
                lines = []
                current_line = []
                for word in words:
                    current_line.append(word)
                    test_line = ' '.join(current_line)
                    bbox = draw.textbbox((0, 0), test_line, font=exp_font)
                    if bbox[2] - bbox[0] > self.config.VIDEO_WIDTH - 120:
                        if len(current_line) > 1:
                            current_line.pop()
                            lines.append(' '.join(current_line))
                            current_line = [word]
                        else:
                            lines.append(word)
                            current_line = []
                if current_line:
                    lines.append(' '.join(current_line))
                
                # Draw explanation lines with background
                for i, line in enumerate(lines[:4]):  # Limit to 4 lines
                    bbox = draw.textbbox((0, 0), line, font=exp_font)
                    line_width = bbox[2] - bbox[0]
                    line_height = bbox[3] - bbox[1]
                    
                    draw.rectangle([50, y_pos - 8, 50 + line_width + 20, y_pos + line_height + 8], 
                                 fill='#E8F5E8', outline='#28A745', width=2)
                    draw.text((70, y_pos), line, fill='#155724', font=exp_font)
                    y_pos += line_height + 20
            
            # Add tutor tip at the bottom
            tip = self._generate_tutor_tip(step, step_number)
            if tip and y_pos < self.config.VIDEO_HEIGHT - 80:
                try:
                    tip_font = ImageFont.truetype("arial.ttf", 22)
                except:
                    tip_font = ImageFont.load_default()
                
                # Draw tip with special styling
                bbox = draw.textbbox((0, 0), tip, font=tip_font)
                line_width = bbox[2] - bbox[0]
                line_height = bbox[3] - bbox[1]
                
                draw.rectangle([50, y_pos - 8, 50 + line_width + 20, y_pos + line_height + 8], 
                             fill='#F8F9FA', outline='#6C757D', width=2)
                draw.text((70, y_pos), tip, fill='#495057', font=tip_font)
            
            return np.array(img)
        
        # Fixed duration for audio synchronization
        duration = 8.0  # Fixed 8 seconds per step to match audio
        return VideoClip(make_frame, duration=duration)
    
    def _extract_key_concept(self, step: Dict[str, Any]) -> str:
        """Extract key mathematical concept from step"""
        description = step.get('description', '').lower()
        explanation = step.get('explanation', '').lower()
        
        # Common mathematical concepts
        concepts = {
            'isolate': 'Isolating the variable',
            'simplify': 'Simplifying expressions',
            'factor': 'Factoring',
            'expand': 'Expanding expressions',
            'substitute': 'Substitution method',
            'eliminate': 'Elimination method',
            'distribute': 'Distributive property',
            'combine': 'Combining like terms',
            'solve': 'Solving equations',
            'equation': 'Equation solving',
            'inequality': 'Inequality solving',
            'quadratic': 'Quadratic formula',
            'slope': 'Finding slope',
            'intercept': 'Finding intercepts',
            'derivative': 'Taking derivatives',
            'integral': 'Integration',
            'limit': 'Finding limits'
        }
        
        for keyword, concept in concepts.items():
            if keyword in description or keyword in explanation:
                return concept
        
        return "Mathematical reasoning"
    
    def _extract_operation(self, step: Dict[str, Any]) -> str:
        """Extract mathematical operation from step"""
        description = step.get('description', '')
        
        # Look for mathematical operations
        if 'add' in description.lower():
            return "Addition (+)"
        elif 'subtract' in description.lower():
            return "Subtraction (-)"
        elif 'multiply' in description.lower():
            return "Multiplication (×)"
        elif 'divide' in description.lower():
            return "Division (÷)"
        elif 'square' in description.lower():
            return "Squaring (x²)"
        elif 'root' in description.lower():
            return "Square root (√)"
        elif 'power' in description.lower():
            return "Exponentiation (x^n)"
        elif 'log' in description.lower():
            return "Logarithm (log)"
        elif 'sin' in description.lower() or 'cos' in description.lower() or 'tan' in description.lower():
            return "Trigonometric function"
        elif 'derivative' in description.lower():
            return "Derivative (d/dx)"
        elif 'integral' in description.lower():
            return "Integral (∫)"
        
        return ""
    
    def _generate_tutor_tip(self, step: Dict[str, Any], step_number: int) -> str:
        """Generate helpful tutor tip for the step"""
        tips = [
            "💡 Remember: Always perform the same operation on both sides of an equation",
            "💡 Tip: Check your work by substituting the answer back into the original equation",
            "💡 Note: Keep track of positive and negative signs carefully",
            "💡 Remember: When dividing, make sure the denominator is not zero",
            "💡 Tip: Simplify before solving to make the problem easier",
            "💡 Note: Look for patterns that can help you solve similar problems",
            "💡 Remember: Show all your work step by step",
            "💡 Tip: Double-check your arithmetic to avoid simple mistakes"
        ]
        
        return tips[step_number % len(tips)]
    
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
        
        return VideoClip(make_frame, duration=3.0)  # Fixed duration to match audio
    
    def _add_audio_narration(self, video_clip: VideoClip, problem_info: Dict[str, Any], solution: Dict[str, Any]) -> VideoClip:
        """Add audio narration to the video with proper synchronization"""
        try:
            # Create separate audio clips for each section
            audio_clips = []
            current_time = 0
            
            # Introduction audio (2 seconds)
            intro_text = f"Welcome to Math Visualization Generator. Let's solve this {problem_info.get('problem_type', 'general')} problem."
            intro_audio = self._create_audio_clip(intro_text, 2.0)
            if intro_audio:
                intro_audio = intro_audio.set_start(current_time)
                audio_clips.append(intro_audio)
            current_time += 2.0
            
            # Problem audio (6 seconds)
            problem_text = f"The problem is: {problem_info.get('original_text', 'No problem provided')}"
            problem_audio = self._create_audio_clip(problem_text, 6.0)
            if problem_audio:
                problem_audio = problem_audio.set_start(current_time)
                audio_clips.append(problem_audio)
            current_time += 6.0
            
            # Solution steps audio (8 seconds per step)
            for i, step in enumerate(solution.get('steps', []), 1):
                step_text = f"Step {i}: {step.get('description', '')}"
                step_audio = self._create_audio_clip(step_text, 8.0)
                if step_audio:
                    step_audio = step_audio.set_start(current_time)
                    audio_clips.append(step_audio)
                current_time += 8.0
            
            # Conclusion audio (3 seconds)
            final_answer = solution.get('final_answer', 'No answer available')
            conclusion_text = f"The final answer is {final_answer}. Thank you for watching."
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
                    # Add silence to match video duration
                    silence_duration = video_clip.duration - combined_audio.duration
                    silence = AudioClip(lambda t: 0, duration=silence_duration)
                    combined_audio = concatenate_audioclips([combined_audio, silence])
                
                # Combine video and audio
                final_video = video_clip.set_audio(combined_audio)
                print(f"Audio narration added successfully! Video duration: {final_video.duration} seconds")
                return final_video
            else:
                print("Audio generation failed, returning video without audio")
                return video_clip
                
        except Exception as e:
            print(f"Error adding audio narration: {e}")
            return video_clip
