import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Mamin API configuration
    MAMIN_API_KEY = os.getenv('MAMIN_API_KEY', 'AIzaSyCOecBtlN7HEruezOrllhn8FNcCxbP-Mfs')
    
    # OpenAI API configuration (fallback)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Video generation settings - optimized for speed
    VIDEO_WIDTH = 1280
    VIDEO_HEIGHT = 720
    FPS = 15
    DURATION_PER_STEP = 3  # seconds per solution step
    
    # Audio settings
    VOICE_RATE = 150  # words per minute
    VOICE_VOLUME = 0.8
    
    # File paths
    UPLOAD_FOLDER = 'uploads'
    OUTPUT_FOLDER = 'outputs'
    TEMP_FOLDER = 'temp'
    
    # Supported image formats
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
    
    # Math problem types
    PROBLEM_TYPES = [
        'algebra',
        'calculus',
        'geometry',
        'trigonometry',
        'statistics',
        'linear_algebra',
        'differential_equations'
    ]
    
    @staticmethod
    def ensure_directories():
        """Create necessary directories if they don't exist"""
        for folder in [Config.UPLOAD_FOLDER, Config.OUTPUT_FOLDER, Config.TEMP_FOLDER]:
            os.makedirs(folder, exist_ok=True)
