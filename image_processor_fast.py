import cv2
import numpy as np
import pytesseract
import easyocr
from PIL import Image
import re
from typing import Tuple, List, Optional

class FastImageProcessor:
    """Fast image processor optimized for speed"""
    
    def __init__(self):
        # Initialize with minimal settings for speed
        self.ocr_reader = easyocr.Reader(['en'], gpu=False)  # Disable GPU for stability
        
    def preprocess_image_fast(self, image_path: str) -> np.ndarray:
        """Fast image preprocessing with minimal operations"""
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Simple thresholding for speed
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
        
    def extract_text_fast(self, image_path: str) -> str:
        """Fast text extraction using optimized OCR settings"""
        try:
            # Preprocess image
            processed_image = self.preprocess_image_fast(image_path)
            
            # Use pytesseract with fast settings
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+-=()[]{}.,;:!? '
            text = pytesseract.image_to_string(processed_image, config=custom_config)
            
            # Clean up text
            cleaned_text = self.clean_text_fast(text)
            
            return cleaned_text
            
        except Exception as e:
            print(f"Fast OCR failed, trying EasyOCR: {e}")
            # Fallback to EasyOCR with minimal settings
            try:
                results = self.ocr_reader.readtext(image_path, detail=0, paragraph=True)
                text = ' '.join(results)
                return self.clean_text_fast(text)
            except Exception as e2:
                print(f"EasyOCR also failed: {e2}")
                return ""
    
    def clean_text_fast(self, text: str) -> str:
        """Fast text cleaning with minimal operations"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common OCR artifacts
        text = re.sub(r'[^\w\s\+\-\=\*\/\(\)\[\]\{\}\.,;:!?]', '', text)
        
        return text.strip()
    
    def extract_text(self, image_path: str) -> str:
        """Main extraction method - uses fast processing"""
        return self.extract_text_fast(image_path)
