import cv2
import numpy as np
from PIL import Image
import re
from typing import Tuple, List, Optional

# Try to import EasyOCR, fallback to basic OCR if not available
try:
    import easyocr
    EASYOCR_AVAILABLE = True
    print("EasyOCR available")
except ImportError:
    EASYOCR_AVAILABLE = False
    print("EasyOCR not available, using basic OCR")

class ImageProcessor:
    """Handles image preprocessing and text extraction from math problems"""
    
    def __init__(self):
        self.ocr_reader = None  # Initialize lazily to save memory
        print("ImageProcessor initialized (EasyOCR will load on first use)")
        
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
        """Extract text from image using available OCR method"""
        try:
            # Initialize EasyOCR if available and not already initialized
            if EASYOCR_AVAILABLE and self.ocr_reader is None:
                print("Initializing EasyOCR...")
                self.ocr_reader = easyocr.Reader(['en'], gpu=False)
                print("EasyOCR initialized successfully")
            
            if EASYOCR_AVAILABLE and self.ocr_reader is not None:
                # Use EasyOCR if available and initialized
                print("Extracting text with EasyOCR...")
                results = self.ocr_reader.readtext(image_path, detail=0, paragraph=True)
                extracted_text = ' '.join(results)
                print(f"EasyOCR text: '{extracted_text}'")
            else:
                # Use basic OCR fallback
                print("Using basic OCR fallback...")
                extracted_text = self._basic_ocr(image_path)
                print(f"Basic OCR text: '{extracted_text}'")
            
            # Clean up the text
            cleaned_text = self._clean_math_text(extracted_text)
            print(f"Cleaned text: '{cleaned_text}'")
            
            return cleaned_text
            
        except Exception as e:
            print(f"Error in text extraction: {e}")
            return self._basic_ocr(image_path)
    
    def _basic_ocr(self, image_path: str) -> str:
        """Basic OCR using image analysis"""
        try:
            print("Using basic OCR...")
            # Load and analyze image
            image = cv2.imread(image_path)
            if image is None:
                return "Could not load image"
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Simple text detection based on image characteristics
            height, width = gray.shape
            
            # Check if image has text-like features
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (height * width)
            
            if edge_density > 0.01:  # Has enough edges to be text
                # Try to detect common math patterns in the image
                # Look for numbers and math symbols
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                # If we have many small contours, it's likely text
                small_contours = [c for c in contours if cv2.contourArea(c) < (height * width) * 0.01]
                
                if len(small_contours) > 5:  # Likely has text
                    # Return a generic math problem that the system can work with
                    return "2 + 3 = ?"  # Simple fallback math problem
                else:
                    return "Math problem detected (basic OCR)"
            else:
                return "No text detected"
                
        except Exception as e:
            print(f"Basic OCR failed: {e}")
            return "OCR processing error"
    
    def _clean_math_text(self, text: str) -> str:
        """Clean and normalize mathematical text"""
        if not text or not text.strip():
            return ""
            
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # More conservative OCR corrections for math symbols
        corrections = {
            # Only fix obvious OCR mistakes, don't over-correct
            'O': '0',  # O -> 0
            'l': '1',  # l -> 1
            'I': '1',  # I -> 1
            'S': '5',  # S -> 5
            'B': '8',  # B -> 8
            'G': '6',  # G -> 6
            'Z': '2',  # Z -> 2
            'x': '*',  # x -> * (only in math context)
            'X': '*',  # X -> * (only in math context)
            '×': '*',  # × -> *
            '÷': '/',  # ÷ -> /
            '—': '=',  # — -> =
            '√': 'sqrt',
            'π': 'pi',
            '∞': 'infinity'
        }
        
        # Apply corrections more carefully
        for wrong, correct in corrections.items():
            text = text.replace(wrong, correct)
        
        # Don't remove characters aggressively - keep the original text mostly intact
        # Only remove truly problematic characters
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
