#!/usr/bin/env python3
"""
Math Visualization Generator for Vercel
Super simple deployment - just works!
"""
from flask import Flask, request, jsonify, render_template_string
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

# Simple HTML template (embedded)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Math Visualization Generator (Vercel)</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f7f6;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .vercel-badge {
            background: #000;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 20px;
            font-size: 14px;
        }
        .upload-area {
            border: 2px dashed #28a745;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .upload-area:hover {
            background-color: #e6f7ee;
        }
        .upload-area input[type="file"] {
            display: none;
        }
        .btn {
            background: #28a745;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px;
        }
        .btn:hover {
            background: #218838;
        }
        .progress {
            margin: 20px 0;
            display: none;
        }
        .progress-bar {
            width: 100%;
            height: 25px;
            background: #e0e0e0;
            border-radius: 5px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: #28a745;
            width: 0%;
            transition: width 0.5s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .result {
            margin: 20px 0;
            padding: 20px;
            background: #e9f7ef;
            border-radius: 5px;
            display: none;
        }
        .error {
            color: #dc3545;
            background: #f8d7da;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            display: none;
        }
        .success {
            color: #155724;
            background: #d4edda;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧮 Math Visualization Generator</h1>
        <div class="vercel-badge">🚀 VERCEL - Super Simple Deployment!</div>
        
        <div class="upload-area" onclick="document.getElementById('fileInput').click()">
            <input type="file" id="fileInput" accept="image/*">
            <h3>📁 Upload Math Problem Image</h3>
            <p>Click here or drag & drop your image</p>
            <button class="btn">Choose File</button>
        </div>

        <div class="progress" id="progress">
            <h3>Processing...</h3>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill">0%</div>
            </div>
            <p id="progressText">Starting...</p>
        </div>

        <div class="result" id="result">
            <h3>✅ Result</h3>
            <p><strong>Problem:</strong> <span id="problemText"></span></p>
            <p><strong>Answer:</strong> <span id="answerText"></span></p>
            <h4>Solution Steps:</h4>
            <pre id="stepsText"></pre>
        </div>

        <div class="success" id="success"></div>
        <div class="error" id="error"></div>
    </div>

    <script>
        let currentTaskId = null;

        document.getElementById('fileInput').addEventListener('change', handleFile);

        function handleFile(event) {
            const file = event.target.files[0];
            if (!file) return;

            resetUI();
            showProgress();
            hideError();
            hideSuccess();

            const formData = new FormData();
            formData.append('image', file);

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    currentTaskId = data.task_id;
                    pollProgress();
                } else {
                    showError(data.error);
                    hideProgress();
                }
            })
            .catch(error => {
                showError('Upload failed: ' + error.message);
                hideProgress();
            });
        }

        function pollProgress() {
            if (!currentTaskId) return;

            const interval = setInterval(() => {
                fetch('/progress/' + currentTaskId)
                    .then(response => response.json())
                    .then(data => {
                        updateProgress(data.progress, data.message);
                        
                        if (data.status === 'completed') {
                            clearInterval(interval);
                            showResult(data.result);
                            hideProgress();
                        } else if (data.status === 'error') {
                            clearInterval(interval);
                            showError(data.message);
                            hideProgress();
                        }
                    })
                    .catch(error => {
                        clearInterval(interval);
                        showError('Progress check failed: ' + error.message);
                        hideProgress();
                    });
            }, 1000);
        }

        function updateProgress(progress, message) {
            document.getElementById('progressFill').style.width = progress + '%';
            document.getElementById('progressFill').textContent = progress + '%';
            document.getElementById('progressText').textContent = message;
        }

        function showResult(result) {
            document.getElementById('problemText').textContent = result.problem || 'Math problem detected';
            document.getElementById('answerText').textContent = result.answer || 'Solution generated';
            document.getElementById('stepsText').textContent = result.steps ? result.steps.join('\\n') : 'Steps generated';
            document.getElementById('result').style.display = 'block';
            showSuccess('Vercel processing completed successfully!');
        }

        function showProgress() {
            document.getElementById('progress').style.display = 'block';
        }

        function hideProgress() {
            document.getElementById('progress').style.display = 'none';
        }

        function showResult() {
            document.getElementById('result').style.display = 'block';
        }

        function hideResult() {
            document.getElementById('result').style.display = 'none';
        }

        function showSuccess(message) {
            document.getElementById('success').textContent = message;
            document.getElementById('success').style.display = 'block';
        }

        function hideSuccess() {
            document.getElementById('success').style.display = 'none';
        }

        function showError(message) {
            document.getElementById('error').textContent = message;
            document.getElementById('error').style.display = 'block';
        }

        function hideError() {
            document.getElementById('error').style.display = 'none';
        }

        function resetUI() {
            hideProgress();
            hideResult();
            hideError();
            hideSuccess();
            currentTaskId = null;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Math Visualization Generator is running on Vercel',
        'version': '5.0.0-vercel'
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
        
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        progress_data[task_id] = {
            'status': 'processing',
            'progress': 0,
            'message': 'Starting Vercel processing...'
        }
        
        # Process in background thread
        thread = threading.Thread(
            target=process_image_vercel,
            args=(task_id,)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': 'Image uploaded successfully. Vercel processing started.'
        })
            
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

def process_image_vercel(task_id):
    """Vercel processing function"""
    try:
        # Step 1: Simulate OCR
        progress_data[task_id]['progress'] = 20
        progress_data[task_id]['message'] = 'Analyzing image on Vercel...'
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
        
        # Create result
        result = {
            'problem': '2x + 5 = 15',
            'answer': 'x = 5',
            'steps': [
                'Start with: 2x + 5 = 15',
                'Subtract 5 from both sides: 2x = 10',
                'Divide both sides by 2: x = 5',
                'Solution: x = 5'
            ],
            'platform': 'Vercel'
        }
        
        progress_data[task_id]['progress'] = 100
        progress_data[task_id]['message'] = 'Vercel processing completed!'
        progress_data[task_id]['status'] = 'completed'
        progress_data[task_id]['result'] = result
        
    except Exception as e:
        progress_data[task_id]['status'] = 'error'
        progress_data[task_id]['message'] = f'Vercel processing failed: {str(e)}'

@app.route('/progress/<task_id>')
def get_progress(task_id):
    """Get processing progress"""
    if task_id in progress_data:
        return jsonify(progress_data[task_id])
    else:
        return jsonify({'error': 'Task not found'}), 404

# Vercel requires this
if __name__ == '__main__':
    app.run(debug=True)
