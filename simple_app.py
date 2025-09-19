#!/usr/bin/env python3
"""
Super simple Math Visualization Generator for Railway
Minimal dependencies, guaranteed to work
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import uuid
import time
import threading
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Progress tracking
progress_data = {}

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page"""
    return render_template('simple_index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Math Visualization Generator is running',
        'version': '3.0.0-simple'
    })

@app.route('/test')
def test_endpoint():
    """Test endpoint for debugging"""
    return jsonify({
        'status': 'ok',
        'message': 'Test endpoint working',
        'timestamp': time.time()
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
                'message': 'Starting simple processing...'
            }
            
            # Process in background thread
            thread = threading.Thread(
                target=process_image_simple,
                args=(filepath, task_id)
            )
            thread.daemon = True
            thread.start()
            
            return jsonify({
                'success': True,
                'task_id': task_id,
                'message': 'Image uploaded successfully. Simple processing started.'
            })
        else:
            return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, BMP, or TIFF'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

def process_image_simple(filepath, task_id):
    """Simple processing function - no external dependencies"""
    try:
        # Step 1: Simulate OCR
        progress_data[task_id]['progress'] = 20
        progress_data[task_id]['message'] = 'Analyzing image...'
        time.sleep(1)
        
        # Step 2: Simulate math parsing
        progress_data[task_id]['progress'] = 40
        progress_data[task_id]['message'] = 'Detecting math problem...'
        time.sleep(1)
        
        # Step 3: Simulate solution generation
        progress_data[task_id]['progress'] = 60
        progress_data[task_id]['message'] = 'Generating solution...'
        time.sleep(1)
        
        # Step 4: Create result
        progress_data[task_id]['progress'] = 80
        progress_data[task_id]['message'] = 'Creating result...'
        time.sleep(1)
        
        # Create simple result
        result = {
            'problem': '2x + 5 = 15',
            'answer': 'x = 5',
            'steps': [
                'Start with: 2x + 5 = 15',
                'Subtract 5 from both sides: 2x = 10',
                'Divide both sides by 2: x = 5',
                'Solution: x = 5'
            ],
            'verification': '2(5) + 5 = 10 + 5 = 15 ✓'
        }
        
        progress_data[task_id]['progress'] = 100
        progress_data[task_id]['message'] = 'Simple processing completed!'
        progress_data[task_id]['status'] = 'completed'
        progress_data[task_id]['result'] = result
        
        print(f"Simple processing completed: {result}")
        
    except Exception as e:
        progress_data[task_id]['status'] = 'error'
        progress_data[task_id]['message'] = f'Simple processing failed: {str(e)}'
        print(f"Simple processing error: {e}")

@app.route('/progress/<task_id>')
def get_progress(task_id):
    """Get processing progress"""
    if task_id in progress_data:
        return jsonify(progress_data[task_id])
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/api/history')
def get_history():
    """Get demo history"""
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
        print(f"Starting simple app on port {port}")
        print("Railway deployment ready!")
        
        app.run(debug=False, host='0.0.0.0', port=port)
        
    except Exception as e:
        print(f"Failed to start app: {e}")
        import traceback
        traceback.print_exc()
        raise
