#!/usr/bin/env python3
"""
Math Visualization Generator Backend API for Railway
Handles OCR, math solving, and video generation
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import time
import threading
from werkzeug.utils import secure_filename
import json
from real_ocr import RealOCRProcessor
from real_math_solver import RealMathSolver

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Progress tracking
progress_data = {}

# Initialize real components
ocr_processor = RealOCRProcessor()
math_solver = RealMathSolver()

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Math Visualization Generator API is running on Railway',
        'version': '6.0.0-railway-api'
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
            # Save file
            filename = secure_filename(file.filename)
            os.makedirs('uploads', exist_ok=True)
            filepath = os.path.join('uploads', filename)
            file.save(filepath)
            
            # Generate unique task ID
            task_id = str(uuid.uuid4())
            progress_data[task_id] = {
                'status': 'processing',
                'progress': 0,
                'message': 'Starting Railway API processing...'
            }
            
            # Process in background thread
            thread = threading.Thread(
                target=process_image_railway,
                args=(filepath, task_id)
            )
            thread.daemon = True
            thread.start()
            
            return jsonify({
                'success': True,
                'task_id': task_id,
                'message': 'Image uploaded successfully. Railway API processing started.'
            })
        else:
            return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, BMP, or TIFF'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

def process_image_railway(filepath, task_id):
    """Railway API processing function with REAL features"""
    try:
        # Step 1: Real OCR
        progress_data[task_id]['progress'] = 20
        progress_data[task_id]['message'] = 'Extracting text from image...'
        
        extracted_text = ocr_processor.extract_text(filepath)
        print(f"Extracted text: '{extracted_text}'")
        
        if not extracted_text or extracted_text.strip() == "":
            progress_data[task_id]['status'] = 'error'
            progress_data[task_id]['message'] = 'Could not extract text from image. Please ensure the image contains clear mathematical text.'
            return
        
        # Step 2: Real math parsing
        progress_data[task_id]['progress'] = 40
        progress_data[task_id]['message'] = 'Parsing mathematical problem...'
        
        # Determine problem type
        problem_type = 'linear_equation'  # Default
        if '^2' in extracted_text or '²' in extracted_text:
            problem_type = 'quadratic_equation'
        elif '+' in extracted_text or '-' in extracted_text:
            problem_type = 'simple_arithmetic'
        elif '=' in extracted_text and any(var in extracted_text for var in ['x', 'y', 'z']):
            problem_type = 'linear_equation'
        
        problem_info = {
            'type': problem_type,
            'equation': extracted_text,
            'formatted': extracted_text
        }
        
        # Step 3: Real math solving
        progress_data[task_id]['progress'] = 60
        progress_data[task_id]['message'] = 'Generating step-by-step solution...'
        
        solution = math_solver.solve_problem(problem_info)
        print(f"Generated solution: {solution}")
        
        # Step 4: Create result
        progress_data[task_id]['progress'] = 80
        progress_data[task_id]['message'] = 'Creating result...'
        
        result = {
            'problem': extracted_text,
            'answer': solution.get('answer', 'Solution generated'),
            'steps': solution.get('steps', []),
            'verification': solution.get('verification', ''),
            'solution_type': solution.get('solution_type', 'unknown'),
            'video_url': f'/video/{task_id}',
            'platform': 'Railway API'
        }
        
        progress_data[task_id]['progress'] = 100
        progress_data[task_id]['message'] = 'Railway API processing completed!'
        progress_data[task_id]['status'] = 'completed'
        progress_data[task_id]['result'] = result
        
        print(f"Railway API processing completed: {result}")
        
    except Exception as e:
        progress_data[task_id]['status'] = 'error'
        progress_data[task_id]['message'] = f'Railway API processing failed: {str(e)}'
        print(f"Railway API processing error: {e}")
        import traceback
        traceback.print_exc()

@app.route('/progress/<task_id>')
def get_progress(task_id):
    """Get processing progress"""
    if task_id in progress_data:
        return jsonify(progress_data[task_id])
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/video/<task_id>')
def get_video(task_id):
    """Get solution video (placeholder)"""
    return jsonify({
        'message': 'Video generation coming soon!',
        'task_id': task_id,
        'status': 'placeholder'
    })

@app.route('/api/history')
def get_history():
    """Get processing history"""
    return jsonify({
        'success': True,
        'history': [
            {
                'id': 'railway-api-demo-1',
                'timestamp': time.time(),
                'problem': '2x + 5 = 15',
                'solution': 'x = 5',
                'status': 'completed',
                'platform': 'Railway API'
            }
        ]
    })

if __name__ == '__main__':
    try:
        # Ensure directories exist
        print("Creating directories for Railway API...")
        os.makedirs('uploads', exist_ok=True)
        os.makedirs('outputs', exist_ok=True)
        print("Directories created successfully!")
        
        # Run the app
        port = int(os.environ.get('PORT', 5000))
        print(f"Starting Railway API on port {port}")
        print("Railway API deployment ready!")
        
        app.run(debug=False, host='0.0.0.0', port=port)
        
    except Exception as e:
        print(f"Failed to start Railway API: {e}")
        import traceback
        traceback.print_exc()
        raise
