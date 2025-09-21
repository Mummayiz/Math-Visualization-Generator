from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import os
import uuid
import time
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
        'message': 'Math Visualization Generator is running',
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
    
    # Get processing mode (fast or quality)
    fast_mode = request.form.get('fast_mode', 'false').lower() == 'true'
    
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
        output_folder = 'outputs'
        os.makedirs(upload_folder, exist_ok=True)
        os.makedirs(output_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Start processing in background thread with file path
        thread = threading.Thread(target=process_image, args=(file_path, task_id, fast_mode))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': 'Upload successful! Processing...'
        })
        
    except Exception as e:
        progress_data[task_id]['status'] = 'error'
        progress_data[task_id]['message'] = f'Upload failed: {str(e)}'
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

def process_image(file_path, task_id, fast_mode=False):
    """Process uploaded image in background thread"""
    try:
        # Update progress
        progress_data[task_id]['progress'] = 10
        progress_data[task_id]['message'] = 'File saved, starting processing...'
        
        # Simulate OCR processing
        progress_data[task_id]['progress'] = 30
        progress_data[task_id]['message'] = 'Extracting text from image...'
        time.sleep(1)
        
        # Simulate math parsing
        progress_data[task_id]['progress'] = 50
        progress_data[task_id]['message'] = 'Parsing math problem...'
        time.sleep(1)
        
        # Simulate solving
        progress_data[task_id]['progress'] = 70
        progress_data[task_id]['message'] = 'Solving problem...'
        time.sleep(1)
        
        # Simulate video generation
        progress_data[task_id]['progress'] = 90
        progress_data[task_id]['message'] = 'Generating video...'
        time.sleep(1)
        
        # Complete processing
        progress_data[task_id]['progress'] = 100
        progress_data[task_id]['status'] = 'completed'
        progress_data[task_id]['message'] = 'Processing completed!'
        progress_data[task_id]['result'] = {
            'problem': {
                'problem_type': 'linear_equation',
                'original_text': '2x + 5 = 13'
            },
            'solution': {
                'steps': [
                    'Subtract 5 from both sides: 2x = 8',
                    'Divide both sides by 2: x = 4'
                ],
                'final_answer': 'x = 4'
            },
            'video_path': 'demo_video.mp4',
            'filename': os.path.basename(file_path)
        }
        
    except Exception as e:
        progress_data[task_id]['status'] = 'error'
        progress_data[task_id]['message'] = f'Error processing image: {str(e)}'

@app.route('/progress/<task_id>')
def get_progress(task_id):
    """Get progress for a specific task"""
    if task_id not in progress_data:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(progress_data[task_id])

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated video file"""
    try:
        file_path = os.path.join('outputs', filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500

@app.route('/view/<filename>')
def view_file(filename):
    """View generated video file"""
    try:
        file_path = os.path.join('outputs', filename)
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error viewing file: {str(e)}'}), 500

@app.route('/api/history')
def get_history():
    """Get all history items"""
    return jsonify({
        'success': True,
        'history': []
    })

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    
    print("Starting Math Visualization Generator...")
    print("App should be accessible at:")
    print("  - http://localhost:5000")
    print("  - http://0.0.0.0:5000")
    print("Health check available at: /health")
    
    app.run(debug=False, host='0.0.0.0', port=5000)
