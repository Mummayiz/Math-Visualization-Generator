#!/usr/bin/env python3
"""
Create a simple test image with math text
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image():
    """Create a simple test image with math text"""
    # Create a white image
    width, height = 400, 100
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        try:
            font = ImageFont.truetype("Arial.ttf", 24)
        except:
            font = ImageFont.load_default()
    
    # Draw math text
    math_text = "2 + 3 = 5"
    text_bbox = draw.textbbox((0, 0), math_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Center the text
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), math_text, fill='black', font=font)
    
    # Save the image
    image_path = "test_math.png"
    image.save(image_path)
    print(f"Created test image: {image_path}")
    return image_path

if __name__ == "__main__":
    create_test_image()
