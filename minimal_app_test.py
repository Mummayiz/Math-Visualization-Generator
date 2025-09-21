#!/usr/bin/env python3
"""Minimal version of your app to test route registration"""

from flask import Flask, request, jsonify, render_template, send_file, Response
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

if __name__ == '__main__':
    print("Starting minimal app...")
    app.run(debug=True, host='0.0.0.0', port=5000)
