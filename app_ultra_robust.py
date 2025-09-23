#!/usr/bin/env python3
"""
Ultra-Robust Math Visualization Generator
Handles threading issues and provides stable operation
"""

import os
import sys
import uuid
import time
import threading
import traceback
from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
import json
from datetime import datetime

# Set matplotlib backend before importing
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

# Import components
try:
    from config import Config
    from image_processor import ImageProcessor
    from math_parser import MathParser
    from solution_engine import SolutionEngine
    from visualizer import MathVisualizer
    from enhanced_educational_video_generator import EnhancedEducationalVideoGenerator
    from educational_video_generator import EducationalVideoGenerator
    from history_manager import HistoryManager
    print("✅ All components imported successfully")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Global variables
tasks = {}
processing_lock = threading.Lock()

# Initialize components
print("🔧 Initializing components...")
try:
    image_processor = ImageProcessor()
    print("✅ ImageProcessor initialized")
    
    math_parser = MathParser()
    print("✅ MathParser initialized")
    
    solution_engine = SolutionEngine()
    print("✅ SolutionEngine initialized")
    
    visualizer = MathVisualizer()
    print("✅ MathVisualizer initialized")
    
    enhanced_video_generator = EnhancedEducationalVideoGenerator()
    print("✅ EnhancedEducationalVideoGenerator initialized")
    
    video_generator = EducationalVideoGenerator()
    print("✅ EducationalVideoGenerator initialized")
    
    history_manager = HistoryManager()
    print("✅ HistoryManager initialized")
    
    print("🎉 All components initialized successfully!")
except Exception as e:
    print(f"❌ Component initialization failed: {e}")
    traceback.print_exc()
    sys.exit(1)

def process_image_ultra_safe(file_path, task_id):
    """Ultra-safe image processing with comprehensive error handling"""
    try:
        print(f"🔄 Starting ultra-safe processing for task {task_id}")
        
        # Update progress
        with processing_lock:
            tasks[task_id]['progress'] = 10
            tasks[task_id]['message'] = 'Extracting text from image...'
        
        # Step 1: Extract text
        print("📝 Extracting text...")
        extracted_text = image_processor.extract_text(file_path)
        print(f"Extracted text: {extracted_text}")
        
        with processing_lock:
            tasks[task_id]['progress'] = 30
            tasks[task_id]['message'] = 'Parsing mathematical problem...'
        
        # Step 2: Parse problem
        print("🧮 Parsing problem...")
        problem_info = math_parser.parse_problem(extracted_text)
        print(f"Problem info: {problem_info}")
        
        with processing_lock:
            tasks[task_id]['progress'] = 50
            tasks[task_id]['message'] = 'Generating solution...'
        
        # Step 3: Generate solution
        print("💡 Generating solution...")
        solution = solution_engine.solve_problem(problem_info)
        print(f"Solution: {solution}")
        
        with processing_lock:
            tasks[task_id]['progress'] = 70
            tasks[task_id]['message'] = 'Creating visualization...'
        
        # Step 4: Create visualization (skip if error)
        print("📊 Creating visualization...")
        try:
            visualization_path = visualizer.create_problem_visualization(problem_info)
            print(f"Visualization created: {visualization_path}")
        except Exception as e:
            print(f"⚠️ Visualization failed: {e}")
            visualization_path = None
        
        with processing_lock:
            tasks[task_id]['progress'] = 80
            tasks[task_id]['message'] = 'Generating educational video...'
        
        # Step 5: Generate video
        print("🎬 Generating video...")
        video_filename = None
        try:
            print(f"🎬 Attempting enhanced video generation for task {task_id}")
            video_filename = enhanced_video_generator.generate_educational_video(problem_info, solution, task_id)
            print(f"✅ Enhanced video generation SUCCESS: {video_filename}")
        except Exception as e:
            print(f"❌ Enhanced video generation FAILED: {e}")
            try:
                print(f"🎬 Attempting fallback video generation for task {task_id}")
                video_filename = video_generator.generate_educational_video(problem_info, solution, task_id)
                print(f"✅ Fallback video generation SUCCESS: {video_filename}")
            except Exception as e2:
                print(f"❌ Fallback video generation also FAILED: {e2}")
                video_filename = None
        
        # Step 6: Save to history
        try:
            history_manager.save_question(
                image_filename=os.path.basename(file_path),
                extracted_text=extracted_text,
                problem_info=problem_info,
                solution=solution,
                video_filename=video_filename
            )
            print("✅ Saved to history")
        except Exception as e:
            print(f"⚠️ History save failed: {e}")
        
        # Final result
        result = {
            'success': True,
            'extracted_text': extracted_text,
            'problem_info': problem_info,
            'solution': solution,
            'visualization_path': str(visualization_path) if visualization_path else None,
            'video_filename': video_filename,
            'video_path': video_filename,  # Add this for frontend compatibility
            'task_id': task_id
        }
        
        with processing_lock:
            tasks[task_id]['progress'] = 100
            tasks[task_id]['message'] = 'Processing completed successfully!'
            tasks[task_id]['result'] = result
            tasks[task_id]['status'] = 'completed'
        
        print(f"🎉 Ultra-safe processing completed successfully for task {task_id}")
        return result
        
    except Exception as e:
        print(f"❌ Ultra-safe processing failed: {e}")
        traceback.print_exc()
        
        with processing_lock:
            tasks[task_id]['progress'] = 0
            tasks[task_id]['message'] = f'Processing failed: {str(e)}'
            tasks[task_id]['status'] = 'error'
            tasks[task_id]['error'] = str(e)
        
        return None

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Ultra-Robust Educational Math Video Generator is running',
        'version': '3.1',
        'features': [
            'Ultra-reliable OCR',
            'Accurate problem parsing',
            'Mathematical solving',
            'Educational video generation',
            'Thread-safe processing'
        ]
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and start processing"""
    try:
        print(f"🔍 Debug: Request files: {list(request.files.keys())}")
        print(f"🔍 Debug: Request form: {list(request.form.keys())}")
        print(f"🔍 Debug: Request content type: {request.content_type}")
        
        if 'file' not in request.files:
            print("❌ Debug: 'file' not found in request.files")
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        print(f"🔍 Debug: File object: {file}")
        print(f"🔍 Debug: File filename: {file.filename}")
        
        if file.filename == '':
            print("❌ Debug: File filename is empty")
            return jsonify({'error': 'No file selected'}), 400
        
        if file:
            # Generate unique task ID
            task_id = str(uuid.uuid4())
            
            # Save file
            filename = secure_filename(file.filename)
            file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            # Initialize task
            with processing_lock:
                tasks[task_id] = {
                    'status': 'processing',
                    'progress': 0,
                    'message': 'Starting processing...',
                    'result': None,
                    'error': None
                }
            
            # Start processing in a separate thread
            def process_thread():
                try:
                    process_image_ultra_safe(file_path, task_id)
                except Exception as e:
                    print(f"❌ Thread processing failed: {e}")
                    traceback.print_exc()
                    with processing_lock:
                        tasks[task_id]['status'] = 'error'
                        tasks[task_id]['error'] = str(e)
            
            thread = threading.Thread(target=process_thread)
            thread.daemon = True
            thread.start()
            
            return jsonify({
                'task_id': task_id,
                'message': 'File uploaded successfully, processing started'
            })
    
    except Exception as e:
        print(f"❌ Upload error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/progress/<task_id>')
def get_progress(task_id):
    """Get processing progress"""
    try:
        with processing_lock:
            if task_id not in tasks:
                return jsonify({'error': 'Task not found'}), 404
            
            task = tasks[task_id]
            response_data = {
                'task_id': task_id,
                'status': task['status'],
                'progress': task['progress'],
                'message': task['message'],
                'result': task.get('result'),
                'error': task.get('error')
            }
            print(f"🔍 Debug: Progress response for {task_id}: {response_data}")
            return jsonify(response_data)
    
    except Exception as e:
        print(f"❌ Progress error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated files"""
    try:
        file_path = os.path.join(Config.OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/view/<filename>')
def view_file(filename):
    """View generated files"""
    try:
        file_path = os.path.join(Config.OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            if filename.endswith('.mp4'):
                return send_file(file_path, mimetype='video/mp4')
            elif filename.endswith('.gif'):
                return send_file(file_path, mimetype='image/gif')
            else:
                return send_file(file_path)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def get_history():
    """Get processing history"""
    try:
        history = history_manager.load_history()
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)
    
    print("🎓 Ultra-Robust Educational Math Video Generator v3.1")
    print("============================================================")
    print("🚀 Starting ultra-robust server...")
    print("App should be accessible at:")
    print("  - http://localhost:5000")
    print("  - http://0.0.0.0:5000")
    print("Health check available at: /health")
    
    # Run with threading enabled
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
