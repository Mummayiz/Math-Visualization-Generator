#!/usr/bin/env python3
"""
Test OCR directly on the math problem image
"""

from image_processor import ImageProcessor

def test_ocr_direct():
    """Test OCR directly on the math problem image"""
    
    processor = ImageProcessor()
    
    print("Testing OCR on test_math_problem.png...")
    extracted_text = processor.extract_text("test_math_problem.png")
    
    print(f"Extracted text: '{extracted_text}'")
    
    if extracted_text and extracted_text != "No text detected":
        print("✅ OCR is working!")
    else:
        print("❌ OCR is not working properly")

if __name__ == "__main__":
    test_ocr_direct()
