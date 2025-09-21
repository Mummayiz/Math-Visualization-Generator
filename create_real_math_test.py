#!/usr/bin/env python3
"""
Create a real math problem test image for testing OCR accuracy
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_math_test_image():
    """Create a test image with a clear math problem"""
    
    # Create a white background
    width, height = 800, 600
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a clear font
    try:
        font_large = ImageFont.truetype("arial.ttf", 48)
        font_medium = ImageFont.truetype("arial.ttf", 36)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    title = "Math Problem"
    bbox = draw.textbbox((0, 0), title, font=font_large)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, 50), title, fill='black', font=font_large)
    
    # Math problem
    problem = "50 + 5 = ?"
    bbox = draw.textbbox((0, 0), problem, font=font_large)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, 200), problem, fill='black', font=font_large)
    
    # Instructions
    instructions = "Solve this addition problem step by step"
    bbox = draw.textbbox((0, 0), instructions, font=font_medium)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, 300), instructions, fill='blue', font=font_medium)
    
    # Additional problem
    problem2 = "What is 50 + 5?"
    bbox = draw.textbbox((0, 0), problem2, font=font_medium)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, 400), problem2, fill='darkgreen', font=font_medium)
    
    # Save the image
    output_path = "test_math_problem.png"
    img.save(output_path)
    print(f"Created test image: {output_path}")
    return output_path

if __name__ == "__main__":
    create_math_test_image()
