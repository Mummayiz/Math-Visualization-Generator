#!/usr/bin/env python3
"""Simple test to check for route conflicts"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Test"

@app.route('/health')
def health_check():
    return "OK"

if __name__ == '__main__':
    print("Testing Flask app...")
    app.run(debug=True, port=5001)
