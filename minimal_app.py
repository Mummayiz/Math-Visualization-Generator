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
    return render_template('minimal_index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Math Visualization Generator is running',
        'version': '2.0.0-minimal'
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
                'message': 'Starting demo processing...'
            }
            
            # Process in background thread
            thread = threading.Thread(
                target=process_image_demo,
                args=(filepath, task_id)
            )
            thread.daemon = True
            thread.start()
            
            return jsonify({
                'success': True,
                'task_id': task_id,
                'message': 'Image uploaded successfully. Demo processing started.'
            })
        else:
            return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, BMP, or TIFF'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

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
