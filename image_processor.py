import cv2
import numpy as np
import pytesseract
import easyocr
from PIL import Image
import re
from typing import Tuple, List, Optional

class ImageProcessor:
    """Handles image preprocessing and text extraction from math problems"""
    
    def __init__(self):
        self.ocr_reader = easyocr.Reader(['en'])
        
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Preprocess image for better OCR results"""
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Morphological operations to clean up
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from image using OCR"""
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_path)
            
            # Use EasyOCR for better math symbol recognition
            results = self.ocr_reader.readtext(processed_image)
            
            # Combine all text
            extracted_text = " ".join([result[1] for result in results])
            
            # Clean up the text
            cleaned_text = self._clean_math_text(extracted_text)
            
            return cleaned_text
            
        except Exception as e:
            print(f"Error in text extraction: {e}")
            return ""
    
    def _clean_math_text(self, text: str) -> str:
        """Clean and normalize mathematical text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Common OCR corrections for math symbols
        corrections = {
            '0': '0', 'O': '0', 'o': '0',
            '1': '1', 'l': '1', 'I': '1',
            '2': '2', 'Z': '2',
            '5': '5', 'S': '5',
            '6': '6', 'G': '6',
            '8': '8', 'B': '8',
            '+': '+', 't': '+',
            '=': '=', '—': '=', '—': '=',
            'x': 'x', 'X': 'x',
            'y': 'y', 'Y': 'y',
            'z': 'z', 'Z': 'z',
            '^': '^', '∧': '^',
            '√': 'sqrt', '√': 'sqrt',
            'π': 'pi', 'π': 'pi',
            '∞': 'infinity', '∞': 'infinity'
        }
        
        for wrong, correct in corrections.items():
            text = text.replace(wrong, correct)
        
        return text
    
    def detect_math_regions(self, image_path: str) -> List[Tuple[int, int, int, int]]:
        """Detect regions in image that likely contain mathematical expressions"""
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Use contour detection to find text regions
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by area and aspect ratio
        math_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = w * h
            aspect_ratio = w / h if h > 0 else 0
            
            # Filter for text-like regions
            if area > 100 and 0.1 < aspect_ratio < 10:
                math_regions.append((x, y, w, h))
        
        return math_regions
    
    def is_math_problem(self, text: str) -> bool:
        """Determine if extracted text contains a mathematical problem"""
        math_indicators = [
            r'\d+',  # Contains numbers
            r'[+\-*/=]',  # Contains operators
            r'[xXyYzZ]',  # Contains variables
            r'solve|find|calculate|compute',  # Contains math keywords
            r'equation|formula|function',  # Contains math terms
        ]
        
        text_lower = text.lower()
        math_score = 0
        
        for pattern in math_indicators:
            if re.search(pattern, text_lower):
                math_score += 1
        
        return math_score >= 2
