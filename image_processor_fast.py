import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
from typing import Tuple, List, Optional

class FastImageProcessor:
    """Fast image processor optimized for speed"""
    
    def __init__(self):
        # Initialize lazily to save memory
        self.ocr_reader = None
        self.tesseract_config = r'--oem 3 --psm 3 -l eng'
        
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
            
            # Try multiple PSM modes for better math text extraction
            configs = [
                '--oem 3 --psm 6 -l eng',  # Default
                '--oem 3 --psm 8 -l eng',  # Single word
                '--oem 3 --psm 7 -l eng',  # Single text line
                '--oem 3 --psm 13 -l eng', # Raw line
            ]
            
            best_text = ""
            for config in configs:
                try:
                    text = pytesseract.image_to_string(processed_image, config=config)
                    if len(text.strip()) > len(best_text.strip()):
                        best_text = text
                except:
                    continue
            
            # Clean up text
            cleaned_text = self.clean_text_fast(best_text)
            
            return cleaned_text
            
        except Exception as e:
            print(f"Fast OCR failed: {e}")
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
        """Main extraction method - uses Tesseract only to save memory"""
        return self.extract_text_fast(image_path)
