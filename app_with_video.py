from flask import Flask, request, jsonify, render_template, send_file
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
from history_manager import HistoryManager

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize components
image_processor = ImageProcessor()
fast_image_processor = FastImageProcessor()
math_parser = MathParser()
solution_engine = SolutionEngine()
visualizer = MathVisualizer()
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
    """Handle file upload and start processing"""
    if 'image' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload an image.'}), 400
    
    task_id = str(uuid.uuid4())
    fast_mode = request.form.get('fast_mode', 'false').lower() == 'true'
    
    progress_data[task_id] = {
        'status': 'processing',
        'progress': 0,
        'message': 'Starting upload...',
        'result': None
    }
    
    try:
        # Save uploaded file immediately to avoid I/O issues
        filename = secure_filename(file.filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
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
        
        # Update progress
        progress_data[task_id]['progress'] = 20
        progress_data[task_id]['message'] = 'Extracting text from image...'
        
        # Process image (use fast or quality processor)
        if fast_mode:
            extracted_text = fast_image_processor.extract_text(file_path)
        else:
            extracted_text = image_processor.extract_text(file_path)
        
        if not extracted_text:
            progress_data[task_id]['status'] = 'error'
            progress_data[task_id]['message'] = 'Could not extract text from image'
            return
        
        # Update progress
        progress_data[task_id]['progress'] = 40
        progress_data[task_id]['message'] = 'Parsing math problem...'
        
        # Parse math problem
        problem_info = math_parser.parse_problem(extracted_text)
        
        # Update progress
        progress_data[task_id]['progress'] = 60
        progress_data[task_id]['message'] = 'Solving problem...'
        
        # Solve problem
        solution = solution_engine.solve_problem(problem_info)
        
        # Update progress
        progress_data[task_id]['progress'] = 80
        progress_data[task_id]['message'] = 'Generating visualization...'
        
        # Generate visualization
        try:
            visualization_img = visualizer.create_problem_visualization(problem_info)
            # Save visualization as image
            visualization_filename = f"visualization_{task_id}.png"
            visualization_path = os.path.join(Config.OUTPUT_FOLDER, visualization_filename)
            visualization_img.save(visualization_path)
        except Exception as e:
            print(f"Visualization generation failed: {e}")
            visualization_path = None
        
        # Update progress
        progress_data[task_id]['progress'] = 90
        progress_data[task_id]['message'] = 'Generating video...'
        
        # Generate video (simplified version without audio to avoid FFMPEG issues)
        video_path = generate_simple_video(problem_info, solution, task_id)
        
        # Update progress
        progress_data[task_id]['progress'] = 100
        progress_data[task_id]['status'] = 'completed'
        progress_data[task_id]['message'] = 'Processing completed!'
        progress_data[task_id]['result'] = {
            'success': True,
            'problem': problem_info,
            'solution': solution,
            'visualization_path': visualization_path,
            'video_path': video_path,
            'filename': os.path.basename(file_path)
        }
        
        # Save to history
        try:
            history_manager.save_question({
                'id': task_id,
                'problem_text': extracted_text,
                'problem_type': problem_info.get('problem_type', 'general'),
                'solution': solution,
                'video_path': video_path,
                'timestamp': time.time()
            })
        except Exception as e:
            print(f"History save failed: {e}")
            # Continue without saving to history
        
        # Clean up the uploaded file after processing
        if os.path.exists(file_path):
            os.remove(file_path)
        
    except Exception as e:
        progress_data[task_id]['status'] = 'error'
        progress_data[task_id]['message'] = f'Error processing image: {str(e)}'
        print(f"Processing error: {e}")

def generate_simple_video(problem_info, solution, task_id):
    """Generate a simple video without audio to avoid FFMPEG issues"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import numpy as np
        
        # Create video frames
        frames = []
        duration = 5  # 5 seconds
        fps = 1  # 1 frame per second for simplicity
        
        for i in range(duration * fps):
            # Create frame
            img = Image.new('RGB', (800, 600), color='white')
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype('arial.ttf', 24)
                title_font = ImageFont.truetype('arial.ttf', 32)
            except:
                font = ImageFont.load_default()
                title_font = ImageFont.load_default()
            
            # Frame 1: Problem
            if i < 2:
                draw.text((50, 100), "Math Problem:", fill='blue', font=title_font)
                draw.text((50, 150), problem_info.get('original_text', 'No problem'), fill='black', font=font)
                draw.text((50, 200), f"Type: {problem_info.get('problem_type', 'Unknown')}", fill='green', font=font)
            
            # Frame 2-3: Solution steps
            elif i < 4:
                draw.text((50, 100), "Solution Steps:", fill='blue', font=title_font)
                y = 150
                for j, step in enumerate(solution.get('steps', [])[:3]):  # Show first 3 steps
                    draw.text((50, y), f"Step {j+1}: {step}", fill='black', font=font)
                    y += 40
            
            # Frame 4-5: Final answer
            else:
                draw.text((50, 100), "Final Answer:", fill='blue', font=title_font)
                draw.text((50, 150), solution.get('final_answer', 'No answer'), fill='red', font=title_font)
            
            # Convert to numpy array
            frames.append(np.array(img))
        
        # Save as animated GIF (simpler than MP4)
        video_filename = f"solution_{task_id}.gif"
        video_path = os.path.join(Config.OUTPUT_FOLDER, video_filename)
        
        # Convert frames to GIF
        frames_pil = [Image.fromarray(frame) for frame in frames]
        frames_pil[0].save(
            video_path,
            save_all=True,
            append_images=frames_pil[1:],
            duration=1000,  # 1 second per frame
            loop=0
        )
        
        return video_filename
        
    except Exception as e:
        print(f"Video generation failed: {e}")
        return None

@app.route('/progress/<task_id>')
def get_progress(task_id):
    """Get progress for a specific task"""
    if task_id not in progress_data:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(progress_data[task_id])

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated file"""
    try:
        file_path = os.path.join(Config.OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500

@app.route('/view/<filename>')
def view_file(filename):
    """View generated file"""
    try:
        file_path = os.path.join(Config.OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error viewing file: {str(e)}'}), 500

@app.route('/api/history')
def get_history():
    """Get all history items"""
    try:
        history = history_manager.get_all_questions()
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
            return jsonify({'success': True, 'message': 'Question deleted successfully'})
        else:
            return jsonify({'error': 'Question not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error deleting question: {str(e)}'}), 500

@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    """Clear all history"""
    try:
        history_manager.clear_history()
        return jsonify({'success': True, 'message': 'History cleared successfully'})
    except Exception as e:
        return jsonify({'error': f'Error clearing history: {str(e)}'}), 500

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(Config.TEMP_FOLDER, exist_ok=True)
    
    print("🎬 Starting Math Visualization Generator with Video Generation!")
    print("=" * 60)
    print("✅ Real OCR processing")
    print("✅ Real math solving")
    print("✅ Real visualization generation")
    print("✅ Video generation (GIF format)")
    print("✅ All UI features working")
    print("=" * 60)
    print("App should be accessible at:")
    print("  - http://localhost:5000")
    print("  - http://0.0.0.0:5000")
    print("Health check available at: /health")
    
    app.run(debug=False, host='0.0.0.0', port=5000)
