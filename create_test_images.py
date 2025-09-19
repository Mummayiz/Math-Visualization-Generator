#!/usr/bin/env python3
"""
Create multiple test images with different math problems
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_test_images():
    """Create multiple test images with different math problems"""
    test_problems = [
        "2 + 3 = 5",
        "x + 5 = 10",
        "3x = 15",
        "x^2 + 2x + 1 = 0",
        "√(x + 5) = 3",
        "2x + 3y = 12"
    ]
    
    for i, problem in enumerate(test_problems):
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
        text_bbox = draw.textbbox((0, 0), problem, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Center the text
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), problem, fill='black', font=font)
        
        # Save the image
        image_path = f"test_math_{i+1}.png"
        image.save(image_path)
        print(f"Created test image {i+1}: {image_path} - '{problem}'")
    
    print(f"\nCreated {len(test_problems)} test images!")
    return [f"test_math_{i+1}.png" for i in range(len(test_problems))]

if __name__ == "__main__":
    create_test_images()
