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
        self.width = 1920  # Increased for better quality
        self.height = 1080  # Full HD for better text readability
        self.fps = 4  # Slightly higher FPS for smoother animation
        self.audio_enabled = AUDIO_AVAILABLE
        
        # Enhanced color scheme for better educational content
        self.colors = {
            'background': '#ffffff',  # Pure white background
            'primary': '#1e40af',     # Professional blue
            'secondary': '#374151',   # Dark gray for text
            'accent': '#3b82f6',      # Bright blue for highlights
            'success': '#059669',     # Green for success
            'warning': '#d97706',     # Orange for warnings
            'error': '#dc2626',       # Red for errors
            'text': '#111827',        # Very dark gray for text
            'light_text': '#6b7280',  # Light gray for secondary text
            'highlight': '#dbeafe',   # Light blue for highlights
            'step_bg': '#f8fafc',     # Very light gray for step backgrounds
            'equation_bg': '#f8fafc', # Very light gray for equation boxes
            'highlight_bg': '#f1f5f9', # Light gray instead of yellow
            'arrow_color': '#3b82f6', # Blue for arrows
            'box_color': '#e5e7eb'    # Light gray for boxes
        }
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize font cache
        self._font_cache = {}
    
    def _get_font(self, size: int):
        """Get font with multiple fallbacks and caching"""
        if size in self._font_cache:
            return self._font_cache[size]
        
        # Try multiple font paths with better quality fonts
        font_paths = [
            'C:/Windows/Fonts/calibri.ttf',  # Better quality font
            'C:/Windows/Fonts/Calibri.ttf',
            'C:/Windows/Fonts/segoeui.ttf',  # Clean, modern font
            'C:/Windows/Fonts/SegoeUI.ttf',
            'C:/Windows/Fonts/arial.ttf',
            'C:/Windows/Fonts/Arial.ttf',
            'C:/Windows/Fonts/consola.ttf',  # Monospace for equations
            'C:/Windows/Fonts/Consola.ttf',
            'arial.ttf',
            'Arial.ttf',
            '/System/Library/Fonts/Arial.ttf',  # macOS
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Linux
        ]
        
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, size)
                self._font_cache[size] = font
                return font
            except (OSError, IOError):
                continue
        
        # If all fail, create a larger default font
        try:
            # Try to load default font with larger size
            font = ImageFont.load_default()
            # Scale up the default font
            if hasattr(font, 'size'):
                scale_factor = size / 10  # Default font is usually size 10
                font = ImageFont.load_default()
            self._font_cache[size] = font
            return font
        except:
            # Last resort - return default
            font = ImageFont.load_default()
            self._font_cache[size] = font
            return font
    
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
            img = Image.new('RGB', (self.width, self.height), color=(255, 255, 255))  # Pure white background
            draw = ImageDraw.Draw(img)
            
            # Enhanced font loading with multiple fallbacks - MUCH LARGER FONTS
            title_font = self._get_font(96)      # Increased from 72
            subtitle_font = self._get_font(64)   # Increased from 48
            text_font = self._get_font(48)       # Increased from 36
            
            # Animated title with fade-in effect
            if i < duration // 2:
                alpha = int(255 * (i / (duration // 2)))
                title_color = (0, 0, 0)  # Black
            else:
                title_color = (0, 0, 0)  # Black
            
            # Main title with animation
            title_text = "🎓 Math Problem Solver"
            title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (self.width - title_width) // 2
            
            # Draw clean title without effects
            draw.text((title_x, 100), title_text, fill=(0, 0, 0), font=title_font)
            
            # Problem type with educational context
            if i > duration // 4:
                problem_type = problem_info.get('problem_type', 'Mathematical Problem')
                type_text = f"Problem Type: {problem_type.title()}"
                type_bbox = draw.textbbox((0, 0), type_text, font=subtitle_font)
                type_width = type_bbox[2] - type_bbox[0]
                type_x = (self.width - type_width) // 2
                
                draw.text((type_x, 200), type_text, fill=(0, 50, 150), font=subtitle_font)  # Dark blue
            
            # Problem statement with enhanced educational formatting
            if i > duration // 2:
                problem_text = problem_info.get('original_text', 'No problem provided')
                # Show characters progressively
                chars_to_show = min(len(problem_text), (i - duration // 2) * 3)
                display_text = problem_text[:chars_to_show]
                
                # Wrap text with better spacing
                wrapped_text = self._wrap_text(display_text, 120)  # Increased from 60 to prevent truncation
                y_pos = 300
                
                # Draw problem statement with educational formatting
                for line_idx, line in enumerate(wrapped_text[:4]):  # Show first 4 lines
                    if line.strip():
                        # Highlight mathematical expressions
                        if any(symbol in line for symbol in ['+', '-', '*', '/', '=', '(', ')', '²', '√', 'x', 'y']):
                            draw.text((50, y_pos), line, fill=(0, 100, 0), font=text_font)  # Green for math
                        else:
                            draw.text((50, y_pos), line, fill=(0, 0, 0), font=text_font)  # Black for text
                        y_pos += 60  # Increased line spacing from 40 to 60 for better readability
                
                # Add cursor effect
                if chars_to_show < len(problem_text) and i % 2 == 0:
                    cursor_x = 50 + draw.textlength(display_text.split('\n')[-1], font=text_font)
                    cursor_y = y_pos - 40
                    draw.text((cursor_x, cursor_y), "|", fill=(0, 0, 0), font=text_font)
            
            # Add decorative elements
            self._add_decorative_elements(draw, i, duration)
            
            frames.append(np.array(img))
        
        return frames
    
    def _create_analysis_frames(self, problem_info: Dict) -> List[np.ndarray]:
        """Create enhanced problem analysis frames with visual breakdown"""
        frames = []
        duration = 3 * self.fps  # 3 seconds
        
        for i in range(duration):
            img = Image.new('RGB', (self.width, self.height), color=(255, 255, 255))  # Pure white background
            draw = ImageDraw.Draw(img)
            
            # Enhanced font loading
            header_font = self._get_font(40)
            text_font = self._get_font(28)
            small_font = self._get_font(20)
            
            # Analysis header with animation
            header_text = "🔍 Problem Analysis & Strategy"
            draw.text((50, 50), header_text, fill=(0, 0, 0), font=header_font)  # Black
            
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
                    
                    # Clean text display without background boxes
                    if i > idx * 8 + 4:
                        # Label
                        draw.text((70, box_y + 10), f"• {label}:", 
                                fill=(0, 0, 0), font=text_font)  # Black
                        
                        # Value with highlighting
                        draw.text((70, box_y + 35), value, 
                                fill=(0, 100, 0), font=small_font)  # Green
            
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
            img = Image.new('RGB', (self.width, self.height), color=(255, 255, 255))  # Pure white background
            draw = ImageDraw.Draw(img)
            
            # Enhanced font loading with proper fallbacks - MUCH LARGER FONTS
            step_font = self._get_font(80)      # Increased from 64 - Much larger step title
            text_font = self._get_font(56)      # Increased from 42 - Much larger main text
            equation_font = self._get_font(72)  # Increased from 56 - Much larger equations
            small_font = self._get_font(40)     # Increased from 32 - Larger small text
            highlight_font = self._get_font(60) # Increased from 48 - New highlight font
            
            # Step header with progress indicator
            progress = step_num / total_steps
            self._draw_progress_bar(draw, progress, i, duration)
            
            # Step title with clean, professional styling
            step_title = f"Step {step_num} of {total_steps}"
            draw.text((120, 120), step_title, 
                     fill=(50, 50, 50), font=step_font)  # Dark gray for professional look
            
            # Step description with enhanced educational formatting
            description = step.get('description', '')
            if description and i > duration // 6:
                chars_to_show = min(len(description), (i - duration // 6) * 3)
                display_text = description[:chars_to_show]
                
                # Wrap text with better spacing
                wrapped_text = self._wrap_text(display_text, 150)  # Increased from 100 to prevent truncation
                y_pos = 200
                
                # Draw each line with educational formatting
                for line_idx, line in enumerate(wrapped_text[:6]):  # Show up to 6 lines
                    if line.strip():
                        # Highlight key mathematical terms with different colors
                        if any(term in line.lower() for term in ['step', 'first', 'next', 'then', 'finally', 'solve', 'calculate']):
                            # Draw key terms in dark blue
                            draw.text((130, y_pos), line, fill=(0, 50, 150), font=text_font)
                        elif any(term in line.lower() for term in ['multiply', 'add', 'subtract', 'divide', 'parentheses', 'order']):
                            # Draw mathematical operations in dark green
                            draw.text((130, y_pos), line, fill=(0, 100, 0), font=text_font)
                        else:
                            # Regular text in black
                            draw.text((130, y_pos), line, fill=(0, 0, 0), font=text_font)
                        y_pos += 70  # Increased line spacing from 50 to 70 for better readability
                
                # Add simple animated cursor without background
                if chars_to_show < len(description) and i % 2 == 0:
                    cursor_x = 130 + draw.textlength(display_text.split('\n')[-1], font=text_font)
                    cursor_y = y_pos - 50
                    # Draw simple cursor without background
                    draw.text((cursor_x, cursor_y), "|", fill=(0, 0, 0), font=text_font)
            
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
            img = Image.new('RGB', (self.width, self.height), color=(255, 255, 255))  # Pure white background
            draw = ImageDraw.Draw(img)
            
            # Enhanced font loading - MUCH LARGER FONTS
            title_font = self._get_font(56)      # Increased from 40
            text_font = self._get_font(40)       # Increased from 28
            large_font = self._get_font(64)      # Increased from 48
            
            # Conclusion header with educational emphasis
            draw.text((50, 50), "🎓 Solution Complete", 
                     fill=(0, 100, 0), font=title_font)  # Green for success
            
            # Final answer with enhanced educational formatting
            final_answer = solution.get('final_answer', 'Solution completed')
            if i > duration // 4:
                # Clean answer display without background boxes
                answer_y = 150
                
                draw.text((70, answer_y), "Final Answer:", 
                         fill=(0, 50, 150), font=text_font)  # Dark blue for label
                
                # Animate answer appearance with educational formatting
                if i > duration // 2:
                    answer_text = str(final_answer)
                    wrapped_answer = self._wrap_text(answer_text, 120)  # Increased from 60 to prevent truncation
                    y_pos = answer_y + 40
                    for line in wrapped_answer[:3]:  # Show up to 3 lines
                        if line.strip():
                            # Highlight mathematical expressions in the answer
                            if any(symbol in line for symbol in ['+', '-', '*', '/', '=', '(', ')', '²', '√', 'x', 'y', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                                draw.text((70, y_pos), line, fill=(0, 100, 0), font=text_font)  # Green for math
                            else:
                                draw.text((70, y_pos), line, fill=(0, 0, 0), font=text_font)  # Black for text
                            y_pos += 50  # Increased line spacing from 35 to 50 for better readability
            
            # Key educational takeaways
            if i > duration // 2:
                takeaways = [
                    "✓ Step-by-step problem solving approach",
                    "✓ Order of operations (PEMDAS) applied correctly",
                    "✓ Mathematical reasoning explained clearly",
                    "✓ Solution verified through systematic approach"
                ]
                
                y_start = 300
                for idx, takeaway in enumerate(takeaways):
                    if i > duration // 2 + idx * 5:
                        # Highlight key educational terms
                        if any(term in takeaway.lower() for term in ['step-by-step', 'pemdas', 'reasoning', 'verified']):
                            draw.text((70, y_start + idx * 60), takeaway, 
                                    fill=(0, 50, 150), font=text_font)  # Dark blue for key terms
                        else:
                            draw.text((70, y_start + idx * 60), takeaway, 
                                    fill=(0, 0, 0), font=text_font)  # Black for regular text
            
            # Add celebration animation
            if i > duration // 3:
                self._add_celebration_elements(draw, i, duration)
            
            frames.append(np.array(img))
        
        return frames
    
    def _draw_progress_bar(self, draw, progress: float, frame: int, duration: int):
        """Draw clean, minimal progress indicator without distracting elements"""
        # Simple text-based progress indicator instead of a bar
        progress_text = f"Processing... {int(progress * 100)}%"
        progress_font = self._get_font(28)
        
        # Calculate text position (top center)
        text_bbox = draw.textbbox((0, 0), progress_text, font=progress_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (self.width - text_width) // 2
        text_y = 30
        
        # Draw clean progress text
        draw.text((text_x, text_y), progress_text, fill=(100, 100, 100), font=progress_font)
    
    def _draw_equation_box(self, draw, equation: str, frame: int, duration: int):
        """Draw enhanced equation display with educational formatting"""
        if not equation:
            return
        
        box_y = 350
        
        # Enhanced equation display with educational formatting
        if frame > duration // 3:
            # Equation label with larger font
            label_font = self._get_font(36)
            equation_font = self._get_font(48)
            
            # Draw "Mathematical Solution:" label
            draw.text((120, box_y), "Mathematical Solution:", 
                     fill=(0, 50, 150), font=label_font)  # Dark blue for emphasis
            
            # Draw equation with enhanced formatting
            equation_text = equation.strip()
            if equation_text:
                # Clean up the equation text
                clean_equation = self._clean_equation_text(equation_text)
                
                # Split equation into lines for better readability
                equation_lines = self._wrap_text(clean_equation, 120)  # Increased from 80 to prevent truncation
                
                y_offset = 0
                for line in equation_lines[:3]:  # Show up to 3 lines
                    if line.strip():
                        # Highlight mathematical symbols and numbers
                        if any(symbol in line for symbol in ['+', '-', '*', '/', '=', '(', ')', '²', '√']):
                            draw.text((120, box_y + 50 + y_offset), line, 
                                     fill=(0, 100, 0), font=equation_font)  # Green for math symbols
                        else:
                            draw.text((120, box_y + 50 + y_offset), line, 
                                     fill=(0, 0, 0), font=equation_font)  # Black for text
                        y_offset += 80  # Increased line spacing from 60 to 80 for better readability
    
    def _highlight_math_operations(self, equation: str) -> str:
        """Highlight mathematical operations in the equation"""
        # This is a simplified version - in a real implementation, you'd parse and highlight
        # For now, we'll just return the equation as-is
        return equation
    
    def _draw_animated_arrows(self, draw, equation: str, box_y: int, slide_offset: int, frame: int):
        """Draw animated arrows pointing to key parts of the equation"""
        if not equation:
            return
        
        # Draw arrows pointing to parentheses, operators, etc.
        arrow_y = box_y + 60
        arrow_color = (0, 0, 0)  # Black
        
        # Simple arrow animation
        if '(' in equation and ')' in equation:
            # Arrow pointing to parentheses
            arrow_x = 200 - slide_offset
            if frame % 20 < 10:  # Blinking effect
                self._draw_arrow(draw, arrow_x, arrow_y, 'right', arrow_color)
        
        if '+' in equation or '*' in equation:
            # Arrow pointing to operators
            arrow_x = 400 - slide_offset
            if frame % 20 < 10:  # Blinking effect
                self._draw_arrow(draw, arrow_x, arrow_y, 'down', arrow_color)
    
    def _draw_arrow(self, draw, x: int, y: int, direction: str, color: str):
        """Draw clean text-based arrow"""
        if direction == 'right':
            # Simple text arrow
            draw.text((x, y), "→", fill=color, font=ImageFont.load_default())
        elif direction == 'down':
            # Simple text arrow
            draw.text((x, y), "↓", fill=color, font=ImageFont.load_default())
    
    def _draw_explanation_box(self, draw, explanation: str, frame: int, duration: int):
        """Draw clean explanation without visual aids"""
        if not explanation:
            return
        
        box_y = 400
        
        if frame > duration // 2:
            # Clean text explanation without background
            wrapped_text = self._wrap_text(explanation, 120)  # Increased from 70 to prevent truncation
            y_pos = box_y + 20
            for line in wrapped_text[:4]:
                draw.text((70, y_pos), line, fill=(0, 0, 0), font=ImageFont.load_default())  # Black
                y_pos += 40  # Increased line spacing from 25 to 40 for better readability
    
    def _draw_arithmetic_diagram(self, draw, problem_info: Dict, frame: int, duration: int):
        """Draw clean text-based diagram for arithmetic problems"""
        # No background text elements - keep it completely clean
        pass
    
    def _add_step_visual_elements(self, draw, step: Dict, step_num: int, frame: int, duration: int):
        """Add clean text-based elements specific to the step content"""
        if frame < duration // 2:
            return
        
        # Clean text-based explanation without visual elements
        description = step.get('description', '').lower()
        
        # No background text elements - keep it completely clean
        pass
    
    def _draw_addition_visual(self, draw, frame: int, duration: int):
        """Draw clean text representation of addition"""
        # No background text elements - keep it completely clean
        pass
    
    def _draw_multiplication_visual(self, draw, frame: int, duration: int):
        """Draw clean text representation of multiplication"""
        # No background text elements - keep it completely clean
        pass
    
    def _add_decorative_elements(self, draw, frame: int, duration: int):
        """Add clean decorative elements to frames"""
        # No decorative elements - keep it clean
        pass
    
    def _add_celebration_elements(self, draw, frame: int, duration: int):
        """Add clean celebration elements to conclusion frames"""
        # No background text elements - keep it completely clean
        pass
    
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
        """Create enhanced audio clip from text using text-to-speech with proper synchronization"""
        if not self.audio_enabled:
            return None
            
        try:
            # Clean and prepare text for better speech synthesis
            clean_text = self._clean_text_for_speech(text)
            if not clean_text.strip():
                return None
                
            # Create temporary audio file
            temp_audio_path = os.path.join(self.output_dir, f"temp_audio_{hash(clean_text) % 10000}.mp3")
            
            # Generate speech with enhanced settings for better quality
            tts = gTTS(text=clean_text, lang='en', slow=False, tld='com')
            tts.save(temp_audio_path)
            
            # Load audio clip
            audio_clip = AudioFileClip(temp_audio_path)
            
            # Ensure audio duration matches video duration exactly
            if audio_clip.duration > duration:
                # If audio is longer, cut it smoothly
                audio_clip = audio_clip.subclip(0, duration)
            elif audio_clip.duration < duration:
                # If audio is shorter, pad with silence to match duration
                silence_duration = duration - audio_clip.duration
                if silence_duration > 0:
                    # Create silence clip
                    silence = AudioFileClip.silent(duration=silence_duration)
                    # Concatenate audio with silence
                    audio_clip = concatenate_audioclips([audio_clip, silence])
            
            # Set volume for better audio quality
            audio_clip = audio_clip.volumex(0.8)
            
            return audio_clip
            
        except Exception as e:
            print(f"❌ Audio generation failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _clean_text_for_speech(self, text: str) -> str:
        """Clean text for better speech synthesis"""
        if not text:
            return ""
        
        # Remove markdown formatting
        clean_text = text.replace('**', '').replace('*', '').replace('`', '')
        clean_text = clean_text.replace('$', '').replace('\\boxed{', 'the answer is ').replace('}', '')
        clean_text = clean_text.replace('\\', '')
        
        # Remove excessive whitespace
        clean_text = ' '.join(clean_text.split())
        
        # Add pauses for better speech flow
        clean_text = clean_text.replace('.', '. ')
        clean_text = clean_text.replace(',', ', ')
        clean_text = clean_text.replace(':', ': ')
        
        return clean_text.strip()
    
    def _add_audio_narration(self, video_path: str, problem_info: Dict, solution: Dict) -> Optional[str]:
        """Add enhanced audio narration to the video with complete coverage"""
        try:
            # Load the video
            video_clip = VideoFileClip(video_path)
            video_duration = video_clip.duration
            
            print(f"🎵 Creating audio narration for {video_duration:.2f} second video...")
            
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
            
            # Solution steps audio - enhanced to cover all steps
            steps = solution.get('steps', [])
            step_duration = 4.0  # 4 seconds per step
            
            for i, step in enumerate(steps):
                # Create comprehensive step narration
                step_text = self._create_step_narration(step, i + 1, len(steps))
                
                step_audio = self._create_audio_clip(step_text, step_duration)
                if step_audio:
                    step_audio = step_audio.set_start(current_time)
                    audio_clips.append(step_audio)
                current_time += step_duration
                
                # Add equation narration if present
                equation = step.get('equation', '')
                if equation and equation.strip():
                    equation_text = f"The equation shows: {equation}"
                    equation_audio = self._create_audio_clip(equation_text, 2.0)
                    if equation_audio:
                        equation_audio = equation_audio.set_start(current_time)
                        audio_clips.append(equation_audio)
                    current_time += 2.0
            
            # Conclusion audio (4 seconds)
            final_answer = solution.get('final_answer', 'The solution is complete.')
            conclusion_text = f"Excellent work! We've solved the problem step by step. The final answer is: {final_answer}. Thank you for learning with us!"
            conclusion_audio = self._create_audio_clip(conclusion_text, 4.0)
            if conclusion_audio:
                conclusion_audio = conclusion_audio.set_start(current_time)
                audio_clips.append(conclusion_audio)
            current_time += 4.0
            
            # Add silence to match video duration if needed
            if current_time < video_duration:
                silence_duration = video_duration - current_time
                if silence_duration > 0:
                    silence = AudioFileClip.silent(duration=silence_duration)
                    silence = silence.set_start(current_time)
                    audio_clips.append(silence)
            
            # Combine all audio clips
            if audio_clips:
                print(f"🎵 Combining {len(audio_clips)} audio clips...")
                combined_audio = concatenate_audioclips(audio_clips)
                
                # Ensure audio duration matches video duration exactly
                if combined_audio.duration > video_duration:
                    combined_audio = combined_audio.subclip(0, video_duration)
                elif combined_audio.duration < video_duration:
                    # Add final silence to match video duration
                    remaining_duration = video_duration - combined_audio.duration
                    if remaining_duration > 0:
                        final_silence = AudioFileClip.silent(duration=remaining_duration)
                        combined_audio = concatenate_audioclips([combined_audio, final_silence])
                
                # Combine video and audio
                final_video = video_clip.set_audio(combined_audio)
                
                # Save the video with audio
                audio_video_path = video_path.replace('.mp4', '_with_audio.mp4')
                print(f"🎵 Saving video with audio to: {audio_video_path}")
                final_video.write_videofile(audio_video_path, codec='libx264', audio_codec='aac', verbose=False, logger=None)
                
                # Clean up
                video_clip.close()
                final_video.close()
                combined_audio.close()
                
                # Replace original video with audio version
                os.replace(audio_video_path, video_path)
                print(f"✅ Audio narration completed successfully!")
                
                return video_path
            else:
                print("❌ No audio clips generated")
                return None
                
        except Exception as e:
            print(f"❌ Error adding audio narration: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _create_step_narration(self, step: Dict, step_num: int, total_steps: int) -> str:
        """Create comprehensive and detailed narration for a step"""
        description = step.get('description', '')
        equation = step.get('equation', '')
        
        # Clean up the description for better speech
        clean_description = description.replace('*', '').replace('**', '').replace('_', '')
        clean_description = clean_description.replace('$', '').replace('\\boxed{', 'the answer is ').replace('}', '')
        clean_description = clean_description.replace('\\', '')
        
        # Create comprehensive narration with educational focus
        narration_parts = []
        
        # Add clear step introduction with context
        narration_parts.append(f"Step {step_num} of {total_steps}")
        
        # Add enhanced description with better explanations
        if clean_description:
            # Enhance mathematical explanations
            enhanced_description = self._enhance_mathematical_explanation(clean_description)
            narration_parts.append(enhanced_description)
            
            # Add specific educational context based on step content
            if "parentheses" in clean_description.lower():
                narration_parts.append("Remember, parentheses tell us to do the operation inside first, before anything else. This is the first rule in the order of operations.")
            elif "multiplication" in clean_description.lower():
                narration_parts.append("Multiplication comes before addition in the order of operations. This ensures we get the correct answer.")
            elif "addition" in clean_description.lower():
                narration_parts.append("Now we can perform the final addition to get our answer. This completes our calculation.")
        
        # Add equation explanation if present
        if equation and equation.strip():
            clean_equation = equation.replace('$', '').replace('\\boxed{', 'the answer is ').replace('}', '')
            clean_equation = clean_equation.replace('\\', '')
            narration_parts.append(f"Let's work through this step by step: {clean_equation}")
            
            # Add specific mathematical reasoning
            if "8 + 4" in clean_equation:
                narration_parts.append("We add 8 and 4 to get 12. This is simple addition within the parentheses.")
            elif "12 * 8" in clean_equation:
                narration_parts.append("We multiply 12 and 8 to get 96. Multiplication comes before addition.")
            elif "8 + 96" in clean_equation:
                narration_parts.append("Finally, we add 8 and 96 to get 104. This is our final answer.")
        
        # Add step-specific educational context
        if step_num == 1:
            narration_parts.append("This first step is crucial because it sets up the foundation for solving the entire problem correctly.")
        elif step_num == 2:
            narration_parts.append("Following the order of operations ensures we get the right answer every time.")
        elif step_num == 3:
            narration_parts.append("Each step builds on the previous one to reach the final solution.")
        
        return '. '.join(narration_parts)
    
    def _enhance_mathematical_explanation(self, text: str) -> str:
        """Enhance mathematical explanations for better clarity and educational value"""
        # Replace common mathematical terms with much clearer, more detailed explanations
        replacements = {
            'PEMDAS': 'P E M D A S, which stands for Parentheses, Exponents, Multiplication, Division, Addition, and Subtraction. This is the fundamental order we must follow when solving any math problem.',
            'BODMAS': 'B O D M A S, which stands for Brackets, Orders, Division, Multiplication, Addition, and Subtraction. This is another way to remember the order of operations.',
            'order of operations': 'the order of operations, which are the fundamental rules that tell us exactly which calculations to perform first in any mathematical expression',
            'parentheses': 'parentheses, which are the curved brackets that group operations together and tell us to solve what\'s inside them first before anything else',
            'multiplication': 'multiplication, which is repeated addition and has higher priority than addition, so we must do it first',
            'addition': 'addition, which is combining numbers together and comes after multiplication in the order of operations',
            'expression': 'mathematical expression, which is a combination of numbers and operations that we need to solve',
            'evaluate': 'solve step by step using the correct order of operations to get the right answer',
            'precedence': 'priority order, which determines which operations must be done first',
            'higher precedence': 'higher priority, meaning this operation must be done before others',
            'group operations': 'group operations together so they are treated as a single unit',
            'fundamental rule': 'basic rule that applies to all mathematical calculations',
            'consistent results': 'the same answer every time, no matter who solves it'
        }
        
        enhanced_text = text
        for term, explanation in replacements.items():
            enhanced_text = enhanced_text.replace(term, explanation)
        
        return enhanced_text
    
    def _clean_equation_text(self, text: str) -> str:
        """Clean equation text for better display"""
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Replace common LaTeX symbols with readable text
        replacements = {
            '\\cdot': ' × ',
            '\\times': ' × ',
            '\\div': ' ÷ ',
            '\\pm': ' ± ',
            '\\sqrt': '√',
            '\\frac': 'fraction',
            '\\sum': 'sum',
            '\\int': 'integral',
            '\\infty': 'infinity',
            '\\alpha': 'α',
            '\\beta': 'β',
            '\\gamma': 'γ',
            '\\pi': 'π',
            '\\theta': 'θ',
            '\\boxed{': 'the answer is ',
            '}': '',
            '$': '',
            '\\': ''
        }
        
        for latex, readable in replacements.items():
            text = text.replace(latex, readable)
        
        return text
