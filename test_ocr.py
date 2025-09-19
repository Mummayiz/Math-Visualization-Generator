#!/usr/bin/env python3
"""
Test OCR functionality locally
"""
import os
import sys
from image_processor import ImageProcessor

def test_ocr(image_path):
    """Test OCR on a specific image"""
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return
    
    print(f"Testing OCR on: {image_path}")
    print("=" * 50)
    
    processor = ImageProcessor()
    
    try:
        # Test text extraction
        extracted_text = processor.extract_text(image_path)
        
        print(f"Extracted text: '{extracted_text}'")
        print(f"Text length: {len(extracted_text.strip())}")
        
        if extracted_text.strip():
            print("✅ OCR successful!")
        else:
            print("❌ No text extracted")
            
    except Exception as e:
        print(f"❌ OCR failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_ocr.py <image_path>")
        print("Example: python test_ocr.py test_image.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    test_ocr(image_path)
