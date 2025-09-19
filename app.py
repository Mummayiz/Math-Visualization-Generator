from flask import Flask, request, jsonify, render_template, send_file, Response
from flask_cors import CORS
import os
import uuid
import time
import threading
from werkzeug.utils import secure_filename
from config import Config
from image_processor import ImageProcessor
from image_processor_fast import FastImageProcessor
from math_parser import MathParser
from solution_engine import SolutionEngine
from visualizer import MathVisualizer
from video_generator import VideoGenerator
from video_generator_fast import FastVideoGenerator
from history_manager import HistoryManager

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize components
image_processor = ImageProcessor()
fast_image_processor = FastImageProcessor()  # Fast image processor
math_parser = MathParser()
solution_engine = SolutionEngine()
visualizer = MathVisualizer()
video_generator = VideoGenerator()
fast_video_generator = FastVideoGenerator()  # Ultra-fast generator
history_manager = HistoryManager()

# Progress tracking
progress_data = {}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    """Upload and process math problem image"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, BMP, or TIFF'}), 400
        
        # Generate unique filename and task ID
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
        task_id = str(uuid.uuid4())
        
        # Get speed mode preference
        fast_mode = request.form.get('fast_mode', 'true').lower() == 'true'
        
        # Save file
        file.save(filepath)
        
        # Initialize progress tracking
        progress_data[task_id] = {
            'status': 'processing',
            'progress': 0,
            'message': 'Starting processing...',
            'result': None
        }
        
        # Process the image in a separate thread
        def process_task():
            try:
                result = process_math_problem_with_progress(filepath, task_id, fast_mode)
                progress_data[task_id]['result'] = result
                progress_data[task_id]['status'] = 'completed'
                progress_data[task_id]['progress'] = 100
                progress_data[task_id]['message'] = 'Processing complete!'
            except Exception as e:
                progress_data[task_id]['status'] = 'error'
                progress_data[task_id]['message'] = f'Error: {str(e)}'
        
        # Start processing thread
        thread = threading.Thread(target=process_task)
        thread.start()
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': 'Processing started'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

def process_math_problem_with_progress(image_path, task_id, fast_mode=True):
    """Process a math problem from image to video with progress tracking"""
    try:
        # Step 1: Extract text from image (10%)
        print("Step 1: Extracting text from image...")
        progress_data[task_id]['progress'] = 10
        progress_data[task_id]['message'] = 'Extracting text from image...'
        
        # Choose image processor based on speed mode
        if fast_mode:
            print("Using fast image processor...")
            extracted_text = fast_image_processor.extract_text(image_path)
        else:
            print("Using high-quality image processor...")
            extracted_text = image_processor.extract_text(image_path)
        
        if not extracted_text:
            return {'error': 'Could not extract text from image. Please ensure the image contains clear mathematical text.'}
        
        # Step 2: Parse the mathematical problem (25%)
        print("Step 2: Parsing mathematical problem...")
        progress_data[task_id]['progress'] = 25
        progress_data[task_id]['message'] = 'Parsing mathematical problem...'
        problem_info = math_parser.parse_problem(extracted_text)
        
        if not problem_info.get('is_math_problem', True):
            return {'error': 'The image does not appear to contain a mathematical problem.'}
        
        # Step 3: Solve the problem (50%)
        print("Step 3: Solving the problem...")
        progress_data[task_id]['progress'] = 50
        progress_data[task_id]['message'] = 'Solving the problem...'
        solution = solution_engine.solve_problem(problem_info)
        
        if not solution.get('steps'):
            return {'error': 'Could not solve the problem. Please check if the problem is mathematically valid.'}
        
        # Step 4: Generate video (75%)
        print("Step 4: Generating educational video...")
        progress_data[task_id]['progress'] = 75
        progress_data[task_id]['message'] = 'Generating educational video...'
        
        # Choose video generator based on speed mode
        if fast_mode:
            print("Using ultra-fast video generator...")
            video_path = fast_video_generator.generate_video(problem_info, solution)
        else:
            print("Using high-quality video generator...")
            video_path = video_generator.generate_video(problem_info, solution)
        
        # Step 5: Finalizing (90%)
        print("Step 5: Finalizing...")
        progress_data[task_id]['progress'] = 90
        progress_data[task_id]['message'] = 'Finalizing...'
        
        # Save to history
        video_filename = os.path.basename(video_path)
        history_id = history_manager.save_question(
            image_filename=os.path.basename(image_path),
            extracted_text=extracted_text,
            problem_info=problem_info,
            solution=solution,
            video_filename=video_filename
        )
        
        # Clean up uploaded file
        os.remove(image_path)
        
        return {
            'success': True,
            'extracted_text': extracted_text,
            'problem_info': problem_info,
            'solution': solution,
            'video_path': video_path,
            'video_filename': video_filename,
            'history_id': history_id
        }
        
    except Exception as e:
        # Clean up uploaded file on error
        if os.path.exists(image_path):
            os.remove(image_path)
        raise e

def process_math_problem(image_path):
    """Process a math problem from image to video (legacy function)"""
    try:
        # Step 1: Extract text from image
        print("Step 1: Extracting text from image...")
        extracted_text = image_processor.extract_text(image_path)
        
        if not extracted_text:
            return {'error': 'Could not extract text from image. Please ensure the image contains clear mathematical text.'}
        
        # Step 2: Parse the mathematical problem
        print("Step 2: Parsing mathematical problem...")
        problem_info = math_parser.parse_problem(extracted_text)
        
        if not problem_info.get('is_math_problem', True):
            return {'error': 'The image does not appear to contain a mathematical problem.'}
        
        # Step 3: Solve the problem
        print("Step 3: Solving the problem...")
        solution = solution_engine.solve_problem(problem_info)
        
        if not solution.get('steps'):
            return {'error': 'Could not solve the problem. Please check if the problem is mathematically valid.'}
        
        # Step 4: Generate video
        print("Step 4: Generating educational video...")
        video_path = video_generator.generate_video(problem_info, solution)
        
        # Clean up uploaded file
        os.remove(image_path)
        
        return {
            'success': True,
            'extracted_text': extracted_text,
            'problem_info': problem_info,
            'solution': solution,
            'video_path': video_path,
            'video_filename': os.path.basename(video_path)
        }
        
    except Exception as e:
        # Clean up uploaded file on error
        if os.path.exists(image_path):
            os.remove(image_path)
        raise e

@app.route('/download/<filename>')
def download_video(filename):
    """Download generated video or slideshow"""
    try:
        # Check if it's a slideshow file
        if filename == 'slideshow.html':
            slideshow_path = os.path.join(Config.OUTPUT_FOLDER, 'slideshow', filename)
            if os.path.exists(slideshow_path):
                return send_file(slideshow_path, as_attachment=True)
            else:
                return jsonify({'error': 'Slideshow file not found'}), 404
        
        # Check for regular video files
        video_path = os.path.join(Config.OUTPUT_FOLDER, filename)
        if os.path.exists(video_path):
            return send_file(video_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500

@app.route('/view/<filename>')
def view_file(filename):
    """View video or slideshow in browser"""
    try:
        # Check if it's a video file
        if filename.endswith('.mp4'):
            video_path = os.path.join(Config.OUTPUT_FOLDER, filename)
            if os.path.exists(video_path):
                return send_file(video_path)
            else:
                return jsonify({'error': 'Video file not found'}), 404
        
        # Check if it's a slideshow file
        elif filename == 'slideshow.html':
            slideshow_path = os.path.join(Config.OUTPUT_FOLDER, 'slideshow', filename)
            if os.path.exists(slideshow_path):
                return send_file(slideshow_path)
            else:
                return jsonify({'error': 'Slideshow file not found'}), 404
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error viewing file: {str(e)}'}), 500

@app.route('/progress/<task_id>')
def get_progress(task_id):
    """Get progress for a specific task"""
    if task_id not in progress_data:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(progress_data[task_id])

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Math Problem Solver is running'})

@app.route('/api/solve', methods=['POST'])
def solve_problem_api():
    """API endpoint to solve math problems from text"""
    try:
        data = request.get_json()
        if not data or 'problem_text' not in data:
            return jsonify({'error': 'Problem text is required'}), 400
        
        problem_text = data['problem_text']
        
        # Parse the problem
        problem_info = math_parser.parse_problem(problem_text)
        
        # Solve the problem
        solution = solution_engine.solve_problem(problem_info)
        
        return jsonify({
            'success': True,
            'problem_info': problem_info,
            'solution': solution
        })
        
    except Exception as e:
        return jsonify({'error': f'Error solving problem: {str(e)}'}), 500

@app.route('/api/history')
def get_history():
    """Get all history entries"""
    try:
        history = history_manager.load_history()
        return jsonify({
            'success': True,
            'history': history
        })
    except Exception as e:
        return jsonify({'error': f'Error loading history: {str(e)}'}), 500

@app.route('/api/history/<question_id>')
def get_history_item(question_id):
    """Get a specific history item by ID"""
    try:
        question = history_manager.get_question_by_id(question_id)
        if question:
            return jsonify({
                'success': True,
                'question': question
            })
        else:
            return jsonify({'error': 'Question not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error loading question: {str(e)}'}), 500

@app.route('/api/history/<question_id>', methods=['DELETE'])
def delete_history_item(question_id):
    """Delete a history item by ID"""
    try:
        success = history_manager.delete_question(question_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Failed to delete question'}), 500
    except Exception as e:
        return jsonify({'error': f'Error deleting question: {str(e)}'}), 500

@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    """Clear all history"""
    try:
        success = history_manager.clear_history()
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Failed to clear history'}), 500
    except Exception as e:
        return jsonify({'error': f'Error clearing history: {str(e)}'}), 500

@app.route('/api/test-ocr', methods=['POST'])
def test_ocr():
    """Test OCR functionality with uploaded image"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Save the file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Test OCR
            processor = ImageProcessor()
            extracted_text = processor.extract_text(filepath)
            
            # Clean up
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'extracted_text': extracted_text,
                'text_length': len(extracted_text.strip())
            })
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        return jsonify({'error': f'OCR test failed: {str(e)}'}), 500

if __name__ == '__main__':
    # Ensure directories exist
    Config.ensure_directories()
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting app on port {port}")
    app.run(debug=False, host='0.0.0.0', port=port)
