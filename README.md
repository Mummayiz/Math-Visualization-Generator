# AI-Powered Math Problem Solver

An intelligent system that converts handwritten or printed math problems into educational solution videos with step-by-step explanations, visual aids, and narration.

## Features

- **Image Processing**: OCR extraction of mathematical text from images
- **Mamin AI Integration**: Advanced mathematical reasoning using Mamin API
- **Mathematical Reasoning**: AI-powered problem solving with step-by-step solutions
- **Visual Generation**: Creates visual representations of mathematical concepts
- **Video Creation**: Generates educational videos with animations and narration
- **Web Interface**: User-friendly web application for easy interaction
- **Multiple Problem Types**: Supports algebra, calculus, geometry, trigonometry, and more
- **Fallback Systems**: Google Math API and local solving as backup options

## Problem Types Supported

- Linear Equations
- Quadratic Equations
- Derivatives and Integrals
- Geometry Problems
- Trigonometry
- Statistics
- General Mathematical Problems

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd math-visualization
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR**:
   - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

4. **Set up environment variables**:
   ```bash
   cp env_example.txt .env
   # The Mamin API key is already configured in env_example.txt
   # Add your OpenAI API key as a fallback if needed
   ```

5. **Create necessary directories**:
   ```bash
   mkdir uploads outputs temp
   ```

## Usage

### Web Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and go to `http://localhost:5000`

3. **Upload an image** containing a math problem

4. **Wait for processing** (the system will extract text, solve the problem, and generate a video)

5. **Download your educational video** with step-by-step solutions

### API Usage

You can also use the system programmatically:

```python
from image_processor import ImageProcessor
from math_parser import MathParser
from solution_engine import SolutionEngine
from video_generator import VideoGenerator

# Process an image
processor = ImageProcessor()
text = processor.extract_text('path/to/image.jpg')

# Parse the problem
parser = MathParser()
problem_info = parser.parse_problem(text)

# Solve the problem
solver = SolutionEngine()
solution = solver.solve_problem(problem_info)

# Generate video
generator = VideoGenerator()
video_path = generator.generate_video(problem_info, solution)
```

## Configuration

Edit `config.py` to customize:

- Video dimensions and quality
- Audio settings
- Supported file formats
- Problem type classifications

## Dependencies

### Core Libraries
- **OpenCV**: Image processing and preprocessing
- **EasyOCR**: Optical Character Recognition
- **SymPy**: Symbolic mathematics
- **Matplotlib**: Mathematical visualizations
- **MoviePy**: Video generation
- **Flask**: Web framework

### AI/ML Libraries
- **Mamin API**: Primary mathematical reasoning engine
- **Google Math API**: Fallback mathematical reasoning
- **OpenAI API**: Advanced mathematical reasoning (fallback)
- **Transformers**: Natural language processing

### Audio/Video
- **gTTS**: Text-to-speech conversion
- **FFmpeg**: Video processing

## File Structure

```
math-visualization/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── image_processor.py    # Image processing and OCR
├── math_parser.py        # Mathematical expression parsing
├── solution_engine.py    # Problem solving engine
├── visualizer.py         # Mathematical visualizations
├── video_generator.py    # Video creation
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html       # Web interface
├── uploads/             # Uploaded images (auto-created)
├── outputs/             # Generated videos (auto-created)
└── temp/               # Temporary files (auto-created)
```

## API Endpoints

- `POST /upload`: Upload and process math problem image
- `GET /download/<filename>`: Download generated video
- `POST /api/solve`: Solve math problem from text
- `GET /health`: Health check

## Example Usage

1. **Upload an image** with a math problem like "Solve for x: 2x + 5 = 13"

2. **The system will**:
   - Extract the text using OCR
   - Parse it as a linear equation
   - Solve it step by step
   - Generate visual representations
   - Create an educational video

3. **Download the video** showing:
   - Problem statement
   - Step 1: "Given equation: 2x + 5 = 13"
   - Step 2: "Subtract 5 from both sides: 2x = 8"
   - Step 3: "Divide by 2: x = 4"
   - Final answer with verification

## Troubleshooting

### Common Issues

1. **OCR not working**: Ensure Tesseract is installed and in PATH
2. **Video generation fails**: Check FFmpeg installation
3. **Audio not working**: Verify gTTS and audio codec support
4. **OpenAI API errors**: Check API key and rate limits

### Error Messages

- "Could not extract text from image": Image quality too low or no text detected
- "Could not solve the problem": Mathematical expression not recognized
- "Video generation failed": Check file permissions and FFmpeg installation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for mathematical reasoning capabilities
- SymPy for symbolic mathematics
- EasyOCR for text extraction
- MoviePy for video generation
- The open-source community for various libraries and tools

## Future Enhancements

- Support for more complex mathematical concepts
- Interactive 3D visualizations
- Multi-language support
- Mobile app development
- Integration with learning management systems
- Real-time collaboration features
