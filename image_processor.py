import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
from typing import Tuple, List, Optional

class ImageProcessor:
    """Handles image preprocessing and text extraction from math problems"""
    
    def __init__(self):
        self.ocr_reader = None  # Initialize lazily to save memory
        
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
        """Extract text from image using Tesseract only to save memory"""
        try:
            # First, try to extract text from the original image without preprocessing
            print("Trying original image...")
            original_text = pytesseract.image_to_string(image_path, config='--oem 3 --psm 6 -l eng')
            print(f"Original image text: '{original_text}'")
            
            # Preprocess image
            processed_image = self.preprocess_image(image_path)
            
            # Use Tesseract for OCR with better math symbol recognition
            # Try multiple PSM modes for better math text extraction
            configs = [
                '--oem 3 --psm 6 -l eng',  # Default
                '--oem 3 --psm 8 -l eng',  # Single word
                '--oem 3 --psm 7 -l eng',  # Single text line
                '--oem 3 --psm 13 -l eng', # Raw line
                '--oem 3 --psm 3 -l eng',  # Fully automatic
                '--oem 3 --psm 4 -l eng',  # Single column
            ]
            
            best_text = original_text if original_text.strip() else ""
            
            for config in configs:
                try:
                    text = pytesseract.image_to_string(processed_image, config=config)
                    print(f"Config {config}: '{text}'")
                    if len(text.strip()) > len(best_text.strip()):
                        best_text = text
                except Exception as e:
                    print(f"Config {config} failed: {e}")
                    continue
            
            extracted_text = best_text
            
            # Debug: Print what we extracted
            print(f"Best OCR text: '{extracted_text}'")
            
            # Clean up the text
            cleaned_text = self._clean_math_text(extracted_text)
            
            # Debug: Print cleaned text
            print(f"Cleaned text: '{cleaned_text}'")
            
            # If we still don't have text, try a simple fallback
            if not cleaned_text.strip():
                print("No text extracted, trying fallback...")
                # Try with minimal processing
                try:
                    fallback_text = pytesseract.image_to_string(image_path, config='--oem 1 --psm 3')
                    cleaned_text = self._clean_math_text(fallback_text)
                    print(f"Fallback text: '{cleaned_text}'")
                except Exception as e:
                    print(f"Fallback also failed: {e}")
            
            return cleaned_text
            
        except Exception as e:
            print(f"Error in text extraction: {e}")
            # Try one more time with absolute minimal config
            try:
                print("Trying minimal config as last resort...")
                minimal_text = pytesseract.image_to_string(image_path, config='--psm 3')
                return self._clean_math_text(minimal_text)
            except Exception as e2:
                print(f"Minimal config also failed: {e2}")
                return ""
    
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
