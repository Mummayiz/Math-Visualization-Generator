#!/usr/bin/env python3
"""
Minimal Math Visualization Generator for Railway deployment
This version works without heavy ML dependencies
"""
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import os
import uuid
import time
import threading
from werkzeug.utils import secure_filename
import json
from real_ocr import RealOCRProcessor
from real_math_parser import RealMathParser
from real_solution_engine import RealSolutionEngine

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Progress tracking
progress_data = {}

# Initialize real components (lazy initialization)
ocr_processor = None
math_parser = None
solution_engine = None

def get_ocr_processor():
    """Get OCR processor with lazy initialization"""
    global ocr_processor
    if ocr_processor is None:
        ocr_processor = RealOCRProcessor()
    return ocr_processor

def get_math_parser():
    """Get math parser with lazy initialization"""
    global math_parser
    if math_parser is None:
        math_parser = RealMathParser()
    return math_parser

def get_solution_engine():
    """Get solution engine with lazy initialization"""
    global solution_engine
    if solution_engine is None:
        solution_engine = RealSolutionEngine()
    return solution_engine

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page"""
    return render_template('minimal_index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Math Visualization Generator is running',
        'version': '2.0.0-minimal'
    })

@app.route('/test')
def test_endpoint():
    """Test endpoint for debugging"""
    try:
        return jsonify({
            'status': 'ok',
            'message': 'Test endpoint working',
            'components': {
                'ocr_processor': ocr_processor is not None,
                'math_parser': math_parser is not None,
                'solution_engine': solution_engine is not None
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/upload', methods=['POST'])
def upload_image():
    """Upload and process math problem image"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join('uploads', unique_filename)
            
            # Ensure uploads directory exists
            os.makedirs('uploads', exist_ok=True)
            file.save(filepath)
            
            # Generate unique task ID
            task_id = str(uuid.uuid4())
            progress_data[task_id] = {
                'status': 'processing',
                'progress': 0,
                'message': 'Starting real processing...'
            }
            
            # Process in background thread
            thread = threading.Thread(
                target=process_image_real,
                args=(filepath, task_id)
            )
            thread.daemon = True
            thread.start()
            
            return jsonify({
                'success': True,
                'task_id': task_id,
                'message': 'Image uploaded successfully. Real processing started.'
            })
        else:
            return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, BMP, or TIFF'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

def process_image_real(filepath, task_id):
    """Real processing function with OCR and math solving"""
    try:
        # Step 1: Extract text from image
        progress_data[task_id]['progress'] = 20
        progress_data[task_id]['message'] = 'Extracting text from image...'
        
        extracted_text = get_ocr_processor().extract_text(filepath)
        print(f"Extracted text: '{extracted_text}'")
        
        if not extracted_text or extracted_text.strip() == "":
            progress_data[task_id]['status'] = 'error'
            progress_data[task_id]['message'] = 'Could not extract text from image. Please ensure the image contains clear mathematical text.'
            return
        
        # Step 2: Parse mathematical problem
        progress_data[task_id]['progress'] = 40
        progress_data[task_id]['message'] = 'Parsing mathematical problem...'
        
        problem_info = get_math_parser().parse_problem(extracted_text)
        print(f"Parsed problem: {problem_info}")
        
        # Step 3: Generate solution
        progress_data[task_id]['progress'] = 60
        progress_data[task_id]['message'] = 'Generating solution...'
        
        solution = get_solution_engine().solve_problem(problem_info)
        print(f"Generated solution: {solution}")
        
        # Step 4: Create result
        progress_data[task_id]['progress'] = 80
        progress_data[task_id]['message'] = 'Creating result...'
        
        result = {
            'problem': extracted_text,
            'problem_info': problem_info,
            'solution': solution,
            'answer': solution.get('answer', 'Solution generated'),
            'steps': solution.get('steps', []),
            'verification': solution.get('verification', ''),
            'solution_type': solution.get('solution_type', 'unknown')
        }
        
        # Step 5: Complete
        progress_data[task_id]['progress'] = 100
        progress_data[task_id]['message'] = 'Processing completed!'
        progress_data[task_id]['status'] = 'completed'
        progress_data[task_id]['result'] = result
        
        print(f"Real processing completed: {result}")
        
    except Exception as e:
        progress_data[task_id]['status'] = 'error'
        progress_data[task_id]['message'] = f'Real processing failed: {str(e)}'
        print(f"Real processing error: {e}")
        import traceback
        traceback.print_exc()

def process_image_demo(filepath, task_id):
    """Demo processing function"""
    try:
        # Simulate processing steps
        steps = [
            (20, "Analyzing image..."),
            (40, "Detecting math problem..."),
            (60, "Generating solution..."),
            (80, "Creating visualization..."),
            (100, "Demo completed!")
        ]
        
        for progress, message in steps:
            time.sleep(1)  # Simulate processing time
            progress_data[task_id]['progress'] = progress
            progress_data[task_id]['message'] = message
        
        # Create demo result
        demo_result = {
            'problem': '2x + 5 = 15',
            'solution': 'x = 5',
            'steps': [
                'Start with: 2x + 5 = 15',
                'Subtract 5 from both sides: 2x = 10',
                'Divide both sides by 2: x = 5',
                'Solution: x = 5'
            ],
            'video_url': '/demo-video'
        }
        
        progress_data[task_id]['status'] = 'completed'
        progress_data[task_id]['message'] = 'Demo processing completed!'
        progress_data[task_id]['result'] = demo_result
        
    except Exception as e:
        progress_data[task_id]['status'] = 'error'
        progress_data[task_id]['message'] = f'Demo processing failed: {str(e)}'

@app.route('/progress/<task_id>')
def get_progress(task_id):
    """Get processing progress"""
    if task_id in progress_data:
        return jsonify(progress_data[task_id])
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/demo-video')
def demo_video():
    """Return a demo video file"""
    # Create a simple demo response
    return jsonify({
        'message': 'Demo video would be generated here',
        'status': 'demo_mode'
    })

@app.route('/api/history')
def get_history():
    """Get processing history"""
    return jsonify({
        'success': True,
        'history': [
            {
                'id': 'demo-1',
                'timestamp': time.time(),
                'problem': '2x + 5 = 15',
                'solution': 'x = 5',
                'status': 'completed'
            }
        ]
    })

if __name__ == '__main__':
    try:
        # Ensure directories exist
        print("Creating directories...")
        os.makedirs('uploads', exist_ok=True)
        os.makedirs('outputs', exist_ok=True)
        print("Directories created successfully!")
        
        # Run the app
        port = int(os.environ.get('PORT', 5000))
        print(f"Starting minimal app on port {port}")
        print("Railway deployment ready!")
        
        app.run(debug=False, host='0.0.0.0', port=port)
        
    except Exception as e:
        print(f"Failed to start app: {e}")
        import traceback
        traceback.print_exc()
        raise
