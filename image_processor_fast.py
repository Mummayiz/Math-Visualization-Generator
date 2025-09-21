import cv2
import numpy as np
import easyocr
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
        """Fast image preprocessing optimized for math text"""
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Enhance contrast for better OCR
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Denoise
        denoised = cv2.medianBlur(enhanced, 3)
        
        # Adaptive thresholding for better text recognition
        thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        return thresh
        
    def extract_text_fast(self, image_path: str) -> str:
        """Fast text extraction using EasyOCR"""
        try:
            # Initialize EasyOCR reader lazily
            if self.ocr_reader is None:
                print("Initializing Fast EasyOCR...")
                self.ocr_reader = easyocr.Reader(['en'], gpu=False)
                print("Fast EasyOCR initialized successfully!")
            
            # Extract text using EasyOCR
            print("Fast extracting text with EasyOCR...")
            results = self.ocr_reader.readtext(image_path, detail=0, paragraph=True)
            
            # Combine all text results
            extracted_text = ' '.join(results)
            print(f"Fast EasyOCR text: '{extracted_text}'")
            
            # Clean up text
            cleaned_text = self.clean_text_fast(extracted_text)
            print(f"Fast cleaned text: '{cleaned_text}'")
            
            return cleaned_text
            
        except Exception as e:
            print(f"Fast OCR failed: {e}")
            return ""
    
    def clean_text_fast(self, text: str) -> str:
        """Fast text cleaning optimized for math expressions"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Fix common OCR mistakes for math
        text = text.replace('O', '0')  # O -> 0
        text = text.replace('l', '1')  # l -> 1
        text = text.replace('I', '1')  # I -> 1
        text = text.replace('S', '5')  # S -> 5
        text = text.replace('B', '8')  # B -> 8
        text = text.replace('G', '6')  # G -> 6
        text = text.replace('Z', '2')  # Z -> 2
        
        # Fix common math symbol mistakes
        text = text.replace('x', '*')  # x -> *
        text = text.replace('X', '*')  # X -> *
        text = text.replace('·', '*')  # · -> *
        text = text.replace('×', '*')  # × -> *
        
        # Keep only math-relevant characters
        text = re.sub(r'[^\w\s\+\-\=\*\/\(\)\[\]\{\}\.,;:!?0-9]', '', text)
        
        # Clean up multiple spaces
        text = re.sub(r'\s+', ' ', text.strip())
        
        return text.strip()
    
    def extract_text(self, image_path: str) -> str:
        """Main extraction method - uses Tesseract only to save memory"""
        return self.extract_text_fast(image_path)
