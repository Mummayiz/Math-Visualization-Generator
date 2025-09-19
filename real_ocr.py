#!/usr/bin/env python3
"""
Real OCR processor for math problems
Uses Tesseract with fallback to basic image analysis
"""
import cv2
import numpy as np
from PIL import Image
import re
from typing import Tuple, List, Optional

class RealOCRProcessor:
    """Real OCR processor for math problems"""
    
    def __init__(self):
        self.tesseract_available = self._check_tesseract()
        print(f"Tesseract available: {self.tesseract_available}")
        
    def _check_tesseract(self):
        """Check if Tesseract is available"""
        try:
            import pytesseract
            # Try to get Tesseract version
            pytesseract.get_tesseract_version()
            return True
        except Exception as e:
            print(f"Tesseract not available: {e}")
            return False
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from image using real OCR"""
        try:
            if self.tesseract_available:
                return self._extract_with_tesseract(image_path)
            else:
                return self._extract_with_basic_analysis(image_path)
        except Exception as e:
            print(f"OCR extraction failed: {e}")
            return self._extract_with_basic_analysis(image_path)
    
    def _extract_with_tesseract(self, image_path: str) -> str:
        """Extract text using Tesseract OCR"""
        try:
            import pytesseract
            
            # Load and preprocess image
            image = cv2.imread(image_path)
            if image is None:
                return "Could not load image"
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply image preprocessing for better OCR
            processed = self._preprocess_image(gray)
            
            # Try multiple OCR configurations
            configs = [
                '--oem 3 --psm 6 -l eng',  # Default
                '--oem 3 --psm 8 -l eng',  # Single word
                '--oem 3 --psm 7 -l eng',  # Single text line
                '--oem 3 --psm 13 -l eng', # Raw line
            ]
            
            best_text = ""
            for config in configs:
                try:
                    text = pytesseract.image_to_string(processed, config=config)
                    if len(text.strip()) > len(best_text.strip()):
                        best_text = text
                except Exception as e:
                    print(f"Tesseract config {config} failed: {e}")
                    continue
            
            # Clean and return text
            cleaned_text = self._clean_math_text(best_text)
            print(f"Tesseract extracted: '{cleaned_text}'")
            return cleaned_text
            
        except Exception as e:
            print(f"Tesseract extraction failed: {e}")
            return self._extract_with_basic_analysis(image_path)
    
    def _extract_with_basic_analysis(self, image_path: str) -> str:
        """Fallback: Basic image analysis for math detection"""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return "Could not load image"
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Analyze image characteristics
            height, width = gray.shape
            
            # Check for text-like features
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (height * width)
            
            # Check for mathematical symbols patterns
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Count potential text regions
            text_regions = 0
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                area = w * h
                aspect_ratio = w / h if h > 0 else 0
                
                # Text-like regions have specific characteristics
                if area > 100 and 0.1 < aspect_ratio < 10:
                    text_regions += 1
            
            # Determine if image contains math
            if edge_density > 0.01 and text_regions > 5:
                return "Math problem detected (basic analysis)"
            elif edge_density > 0.005:
                return "Text detected (basic analysis)"
            else:
                return "No clear text detected"
                
        except Exception as e:
            print(f"Basic analysis failed: {e}")
            return "Image analysis failed"
    
    def _preprocess_image(self, gray_image):
        """Preprocess image for better OCR"""
        try:
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray_image, (3, 3), 0)
            
            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Morphological operations to clean up
            kernel = np.ones((2, 2), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            return cleaned
        except Exception as e:
            print(f"Image preprocessing failed: {e}")
            return gray_image
    
    def _clean_math_text(self, text: str) -> str:
        """Clean and normalize mathematical text"""
        if not text or not text.strip():
            return ""
            
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Common OCR corrections for math symbols
        corrections = {
            '0': '0', 'O': '0', 'o': '0', 'Q': '0',
            '1': '1', 'l': '1', 'I': '1', '|': '1',
            '2': '2', 'Z': '2', 'z': '2',
            '3': '3', 'B': '3', 'E': '3',
            '4': '4', 'A': '4',
            '5': '5', 'S': '5', 's': '5',
            '6': '6', 'G': '6', 'b': '6',
            '7': '7', 'T': '7', 't': '7',
            '8': '8', 'B': '8',
            '9': '9', 'g': '9', 'q': '9',
            '+': '+', 't': '+', 'T': '+',
            '-': '-', '_': '-', '—': '-',
            '=': '=', '—': '=', '—': '=',
            '*': '*', 'x': '*', 'X': '*', '×': '*',
            '/': '/', '\\': '/', '÷': '/',
            'x': 'x', 'X': 'x', '×': 'x',
            'y': 'y', 'Y': 'y',
            'z': 'z', 'Z': 'z',
            '^': '^', '∧': '^', '**': '^',
            '√': 'sqrt', '√': 'sqrt',
            'π': 'pi', 'π': 'pi',
            '∞': 'infinity', '∞': 'infinity',
            '(': '(', ')': ')',
            '[': '[', ']': ']',
            '{': '{', '}': '}',
            '.': '.', ',': ',',
            '?': '?', '!': '!'
        }
        
        for wrong, correct in corrections.items():
            text = text.replace(wrong, correct)
        
        # Remove any remaining non-printable characters except math symbols
        text = re.sub(r'[^\w\s\+\-\=\*\/\(\)\[\]\{\}\.,;:!?^√π∞]', '', text)
        
        return text.strip()
    
    def is_math_problem(self, text: str) -> bool:
        """Determine if extracted text contains a mathematical problem"""
        if not text or not text.strip():
            return False
            
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
