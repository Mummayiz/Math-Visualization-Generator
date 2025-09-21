#!/usr/bin/env python3
"""Test upload functionality"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import uuid
import threading
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Progress tracking
progress_data = {}

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Test Upload App is running',
        'version': '1.0.0'
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload an image.'}), 400
    
    # Generate unique task ID
    task_id = str(uuid.uuid4())
    
    # Initialize progress
    progress_data[task_id] = {
        'status': 'processing',
        'progress': 0,
        'message': 'Starting upload...',
        'result': None
    }
    
    try:
        # Save uploaded file immediately to avoid I/O issues
        filename = secure_filename(file.filename)
        upload_folder = 'uploads'
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Update progress
        progress_data[task_id]['progress'] = 50
        progress_data[task_id]['message'] = 'File saved successfully!'
        
        # Simulate processing
        import time
        time.sleep(2)
        
        # Complete processing
        progress_data[task_id]['progress'] = 100
        progress_data[task_id]['status'] = 'completed'
        progress_data[task_id]['message'] = 'Upload completed successfully!'
        progress_data[task_id]['result'] = {
            'filename': filename,
            'file_path': file_path,
            'message': 'File uploaded and saved successfully!'
        }
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': 'Upload successful!'
        })
        
    except Exception as e:
        progress_data[task_id]['status'] = 'error'
        progress_data[task_id]['message'] = f'Error: {str(e)}'
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/progress/<task_id>')
def get_progress(task_id):
    """Get progress for a specific task"""
    if task_id not in progress_data:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(progress_data[task_id])

if __name__ == '__main__':
    print("Starting Test Upload App...")
    print("App should be accessible at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
