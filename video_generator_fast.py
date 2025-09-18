#!/usr/bin/env python3
"""
Ultra-Fast Video Generator for Math Problem Solver
Optimized for maximum speed with minimal quality loss
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
    import pygame
    AUDIO_AVAILABLE = True
    print("Audio libraries loaded successfully!")
except ImportError as e:
    AUDIO_AVAILABLE = False
    print(f"Audio libraries not available: {e}. Install gtts and pygame for audio support.")

class FastVideoGenerator:
    """Ultra-fast video generator optimized for speed"""
    
    def __init__(self):
        self.config = Config()
        self.ensure_directories()
        self.audio_enabled = AUDIO_AVAILABLE
        self._audio_cache = {}  # Cache for audio clips
        
    def ensure_directories(self):
        """Create necessary directories"""
        Config.ensure_directories()
        
    def _create_fast_audio_clip(self, text: str, duration: float) -> Optional[AudioClip]:
        """Create audio clip with caching for speed"""
        if not self.audio_enabled:
            return None
            
        # Use text hash as cache key
        cache_key = hash(text) % 10000
        
        # Check cache first
        if cache_key in self._audio_cache:
            cached_clip = self._audio_cache[cache_key]
            # Adjust duration if needed
            if cached_clip.duration >= duration:
                return cached_clip.subclip(0, duration)
            else:
                # Pad with silence
                silence_duration = duration - cached_clip.duration
                silence = AudioClip(lambda t: 0, duration=silence_duration)
                return concatenate_audioclips([cached_clip, silence])
        
        try:
            # Create temporary audio file
            temp_audio_path = os.path.join(self.config.TEMP_FOLDER, f"temp_audio_{cache_key}.mp3")
            
            # Skip if file already exists
            if os.path.exists(temp_audio_path):
                audio_clip = AudioFileClip(temp_audio_path)
            else:
                # Generate speech with optimized settings
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(temp_audio_path)
                audio_clip = AudioFileClip(temp_audio_path)
            
            # Cache the clip
            self._audio_cache[cache_key] = audio_clip
            
            # Adjust to match duration exactly
            if audio_clip.duration > duration:
                return audio_clip.subclip(0, duration)
            elif audio_clip.duration < duration:
                silence_duration = duration - audio_clip.duration
                silence = AudioClip(lambda t: 0, duration=silence_duration)
                return concatenate_audioclips([audio_clip, silence])
            
            return audio_clip
            
        except Exception as e:
            print(f"Audio generation failed: {e}")
            return None
    
    def generate_video(self, problem_info: Dict[str, Any], solution: Dict[str, Any]) -> str:
        """Generate ultra-fast video"""
        
        print("Creating ultra-fast video...")
        
        # Create simple video clips with reduced duration
        clips = []
        
        # 1. Fast introduction (1 second)
        print("Creating introduction...")
        intro_clip = self._create_fast_intro(problem_info)
        clips.append(intro_clip)
        
        # 2. Problem presentation (3 seconds)
        print("Creating problem slide...")
        problem_clip = self._create_fast_problem(problem_info)
        clips.append(problem_clip)
        
        # 3. Solution steps (4 seconds each)
        print("Creating solution steps...")
        for i, step in enumerate(solution.get('steps', []), 1):
            print(f"Creating step {i}...")
            step_clip = self._create_fast_step(step, i, len(solution.get('steps', [])))
            clips.append(step_clip)
        
        # 4. Conclusion (2 seconds)
        print("Creating conclusion...")
        conclusion_clip = self._create_fast_conclusion(solution)
        clips.append(conclusion_clip)
        
        # Concatenate all clips
        print("Combining clips...")
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Add audio narration if available (with reduced quality for speed)
        if self.audio_enabled:
            print("Adding audio narration...")
            try:
                final_video = self._add_fast_audio_narration(final_video, problem_info, solution)
                print(f"Audio narration added successfully! Final video duration: {final_video.duration} seconds")
            except Exception as e:
                print(f"Failed to add audio narration: {e}")
                print("Continuing with video without audio...")
        
        # Generate output filename
        output_filename = f"math_solution_{problem_info.get('problem_type', 'general')}.mp4"
        output_path = os.path.join(self.config.OUTPUT_FOLDER, output_filename)
        
        # Write video file with ultra-fast settings
        print("Rendering video (ultra-fast)...")
        final_video.write_videofile(
            output_path,
            fps=12,  # Even lower FPS for speed
            codec='libx264',
            preset='ultrafast',
            ffmpeg_params=['-crf', '28'],  # Higher compression for speed
            verbose=False,
            logger=None,
            write_logfile=False,
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        print(f"Ultra-fast video created: {output_path}")
        return output_filename
    
    def _create_fast_intro(self, problem_info: Dict[str, Any]) -> VideoClip:
        """Create fast introduction slide"""
        
        def make_frame(t):
            img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'white')
            draw = ImageDraw.Draw(img)
            
            # Simple title
            title = "Math Problem Solver"
            try:
                font = ImageFont.truetype("arial.ttf", 50)
            except:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), title, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (self.config.VIDEO_WIDTH - text_width) // 2
            y = (self.config.VIDEO_HEIGHT - text_height) // 2 - 50
            
            draw.text((x, y), title, fill='black', font=font)
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=1.0)  # Reduced duration
    
    def _create_fast_problem(self, problem_info: Dict[str, Any]) -> VideoClip:
        """Create fast problem presentation"""
        
        def make_frame(t):
            img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), '#F8F9FA')
            draw = ImageDraw.Draw(img)
            
            # Simplified header
            title = "Problem Analysis"
            try:
                title_font = ImageFont.truetype("arial.ttf", 40)
            except:
                title_font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), title, font=title_font)
            text_width = bbox[2] - bbox[0]
            
            draw.rectangle([40, 30, self.config.VIDEO_WIDTH - 40, 80], 
                         fill='#2C3E50', outline='#1A252F', width=2)
            draw.text(((self.config.VIDEO_WIDTH - text_width) // 2, 55 - 20), 
                     title, fill='white', font=title_font)
            
            y_pos = 100
            
            # Problem type
            problem_type = problem_info.get('problem_type', 'general')
            type_label = f"Type: {problem_type.title()}"
            try:
                type_font = ImageFont.truetype("arial.ttf", 28)
            except:
                type_font = ImageFont.load_default()
            
            draw.text((60, y_pos), type_label, fill='#0D47A1', font=type_font)
            y_pos += 50
            
            # Problem statement (simplified)
            problem_text = problem_info.get('original_text', 'No problem provided')
            try:
                text_font = ImageFont.truetype("arial.ttf", 32)
            except:
                text_font = ImageFont.load_default()
            
            # Simple text wrapping
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
            
            # Draw problem lines (max 3 lines)
            for i, line in enumerate(lines[:3]):
                bbox = draw.textbbox((0, 0), line, font=text_font)
                line_width = bbox[2] - bbox[0]
                line_height = bbox[3] - bbox[1]
                
                x = (self.config.VIDEO_WIDTH - line_width) // 2
                
                draw.rectangle([x - 20, y_pos - 8, x + line_width + 20, y_pos + line_height + 8], 
                             fill='white', outline='#FF5722', width=2)
                draw.text((x, y_pos), line, fill='#D84315', font=text_font)
                y_pos += line_height + 20
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=3.0)  # Reduced duration
    
    def _create_fast_step(self, step: Dict[str, Any], step_number: int, total_steps: int) -> VideoClip:
        """Create fast step with minimal content"""
        
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
            
            draw.rectangle([40, 20, self.config.VIDEO_WIDTH - 40, 80], 
                         fill='#2E86AB', outline='#1B4F72', width=2)
            draw.text(((self.config.VIDEO_WIDTH - text_width) // 2, 50 - 20), 
                     step_title, fill='white', font=header_font)
            
            y_pos = 100
            
            # Step description (simplified)
            description = step.get('description', '')
            if description:
                try:
                    desc_font = ImageFont.truetype("arial.ttf", 28)
                except:
                    desc_font = ImageFont.load_default()
                
                # Simple text wrapping
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
                
                # Draw description lines (max 2 lines)
                for i, line in enumerate(lines[:2]):
                    bbox = draw.textbbox((0, 0), line, font=desc_font)
                    line_width = bbox[2] - bbox[0]
                    line_height = bbox[3] - bbox[1]
                    
                    draw.rectangle([50, y_pos - 6, 50 + line_width + 20, y_pos + line_height + 6], 
                                 fill='#FFF8E1', outline='#FF9800', width=1)
                    draw.text((70, y_pos), line, fill='#E65100', font=desc_font)
                    y_pos += line_height + 15
                
                y_pos += 20
            
            # Step explanation (simplified)
            explanation = step.get('explanation', '')
            if explanation and y_pos < self.config.VIDEO_HEIGHT - 100:
                try:
                    exp_font = ImageFont.truetype("arial.ttf", 24)
                except:
                    exp_font = ImageFont.load_default()
                
                # Simple text wrapping
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
                
                # Draw explanation lines (max 2 lines)
                for i, line in enumerate(lines[:2]):
                    bbox = draw.textbbox((0, 0), line, font=exp_font)
                    line_width = bbox[2] - bbox[0]
                    line_height = bbox[3] - bbox[1]
                    
                    draw.rectangle([50, y_pos - 6, 50 + line_width + 20, y_pos + line_height + 6], 
                                 fill='#E8F5E8', outline='#28A745', width=1)
                    draw.text((70, y_pos), line, fill='#155724', font=exp_font)
                    y_pos += line_height + 15
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=4.0)  # Reduced duration
    
    def _create_fast_conclusion(self, solution: Dict[str, Any]) -> VideoClip:
        """Create fast conclusion slide"""
        
        def make_frame(t):
            img = Image.new('RGB', (self.config.VIDEO_WIDTH, self.config.VIDEO_HEIGHT), 'lightgreen')
            draw = ImageDraw.Draw(img)
            
            # Title
            title = "Solution Complete!"
            try:
                font = ImageFont.truetype("arial.ttf", 45)
            except:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), title, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (self.config.VIDEO_WIDTH - text_width) // 2
            y = (self.config.VIDEO_HEIGHT - text_height) // 2 - 50
            
            draw.text((x, y), title, fill='black', font=font)
            
            # Final answer
            final_answer = solution.get('final_answer', 'No answer available')
            answer_text = f"Answer: {final_answer}"
            try:
                answer_font = ImageFont.truetype("arial.ttf", 32)
            except:
                answer_font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), answer_text, font=answer_font)
            text_width = bbox[2] - bbox[0]
            x = (self.config.VIDEO_WIDTH - text_width) // 2
            y += text_height + 30
            
            draw.text((x, y), answer_text, fill='darkblue', font=answer_font)
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=2.0)  # Reduced duration
    
    def _add_fast_audio_narration(self, video_clip: VideoClip, problem_info: Dict[str, Any], solution: Dict[str, Any]) -> VideoClip:
        """Add fast audio narration with reduced quality for speed"""
        try:
            # Create separate audio clips for each section
            audio_clips = []
            current_time = 0
            
            # Introduction audio (1 second)
            intro_text = f"Math problem solver. {problem_info.get('problem_type', 'general')} problem."
            intro_audio = self._create_fast_audio_clip(intro_text, 1.0)
            if intro_audio:
                intro_audio = intro_audio.set_start(current_time)
                audio_clips.append(intro_audio)
            current_time += 1.0
            
            # Problem audio (3 seconds)
            problem_text = f"Problem: {problem_info.get('original_text', 'No problem provided')[:100]}..."
            problem_audio = self._create_fast_audio_clip(problem_text, 3.0)
            if problem_audio:
                problem_audio = problem_audio.set_start(current_time)
                audio_clips.append(problem_audio)
            current_time += 3.0
            
            # Solution steps audio (4 seconds per step)
            for i, step in enumerate(solution.get('steps', []), 1):
                step_text = f"Step {i}: {step.get('description', '')[:80]}..."
                step_audio = self._create_fast_audio_clip(step_text, 4.0)
                if step_audio:
                    step_audio = step_audio.set_start(current_time)
                    audio_clips.append(step_audio)
                current_time += 4.0
            
            # Conclusion audio (2 seconds)
            final_answer = solution.get('final_answer', 'No answer available')
            conclusion_text = f"Answer: {final_answer[:50]}..."
            conclusion_audio = self._create_fast_audio_clip(conclusion_text, 2.0)
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
                print(f"Fast audio narration added! Video duration: {final_video.duration} seconds")
                return final_video
            else:
                print("Audio generation failed, returning video without audio")
                return video_clip
                
        except Exception as e:
            print(f"Error adding fast audio narration: {e}")
            return video_clip
    
    def cleanup_cache(self):
        """Clean up audio cache"""
        self._audio_cache.clear()