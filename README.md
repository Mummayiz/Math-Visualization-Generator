# 🧮 Math Visualization Generator

An AI-powered math problem solver that converts handwritten or printed mathematical problems into educational videos with step-by-step explanations.

## ✨ Features

- **📸 Image Processing**: Upload images of math problems (handwritten or printed)
- **🤖 AI-Powered Solving**: Uses Google's Gemini AI for mathematical reasoning
- **🎥 Video Generation**: Creates educational videos with tutor-style explanations
- **📊 Progress Tracking**: Real-time progress updates during processing
- **🎯 Key Concepts**: Highlights important mathematical concepts and operations
- **💡 Tutor Tips**: Provides helpful hints and reasoning for each step
- **📱 Modern UI**: Clean, responsive web interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/math-visualization-generator.git
   cd math-visualization-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   ```
   Edit `.env` and add your API keys:
   ```
   MAMIN_API_KEY=your_google_gemini_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   Navigate to `http://localhost:5000`

## 🎯 How to Use

1. **Upload Image**: Drag and drop or click to upload a math problem image
2. **Watch Progress**: Monitor real-time processing progress (0-100%)
3. **View Video**: Watch the generated educational video with step-by-step explanations
4. **Download**: Save the video for offline viewing

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **AI/ML**: Google Gemini API, OpenAI API, SymPy
- **Image Processing**: EasyOCR, Tesseract, OpenCV, Pillow
- **Video Generation**: MoviePy
- **Frontend**: HTML, CSS, JavaScript
- **Mathematical Processing**: SymPy, NumPy

## 📁 Project Structure

```
math-visualization-generator/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── image_processor.py    # Image processing and OCR
├── math_parser.py        # Mathematical problem parsing
├── solution_engine.py    # AI-powered problem solving
├── video_generator.py    # Educational video generation
├── visualizer.py         # Mathematical visualizations
├── mamin_api.py          # Google Gemini API integration
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Web interface
├── static/               # CSS and JavaScript files
├── outputs/              # Generated videos and images
└── uploads/              # Temporary uploaded files
```

## 🔧 Configuration

### API Keys

The application requires API keys for AI services:

- **Google Gemini API** (Primary): Used for mathematical reasoning
- **OpenAI API** (Fallback): Used when Gemini API is unavailable

### Video Settings

You can customize video generation in `config.py`:

```python
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
FPS = 15
DURATION_PER_STEP = 3  # seconds per solution step
```

## 🎨 Features in Detail

### Image Processing
- Supports multiple image formats (PNG, JPG, JPEG, GIF, BMP, TIFF)
- Handles both handwritten and printed mathematical text
- Automatic image preprocessing for better OCR results

### AI-Powered Solving
- Uses Google's Gemini AI for advanced mathematical reasoning
- Fallback to OpenAI API for reliability
- Local SymPy solving for basic mathematical operations
- Automatic problem type classification

### Video Generation
- Tutor-style educational videos
- Key concept highlighting
- Mathematical operation identification
- Step-by-step reasoning explanations
- Professional visual design

### Progress Tracking
- Real-time progress updates (0-100%)
- Detailed status messages
- Non-blocking processing with threading

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for mathematical reasoning
- OpenAI for fallback AI services
- MoviePy for video generation
- EasyOCR and Tesseract for text extraction
- SymPy for symbolic mathematics
- Flask for the web framework

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/math-visualization-generator/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

## 🔮 Future Enhancements

- [ ] Support for more mathematical problem types
- [ ] Interactive video controls
- [ ] Batch processing of multiple images
- [ ] Custom video templates
- [ ] Mobile app version
- [ ] Integration with learning management systems

---

**Made with ❤️ for mathematics education**