#!/usr/bin/env python3
"""
Setup script for AI Math Problem Solver with Mamin integration
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} is compatible")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    return run_command("pip install -r requirements.txt", "Installing Python packages")

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    directories = ['uploads', 'outputs', 'temp']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    return True

def setup_environment():
    """Set up environment file"""
    print("\n🔧 Setting up environment...")
    if not os.path.exists('.env'):
        if os.path.exists('env_example.txt'):
            import shutil
            shutil.copy('env_example.txt', '.env')
            print("✅ Created .env file from env_example.txt")
        else:
            print("⚠️  env_example.txt not found, creating basic .env file")
            with open('.env', 'w') as f:
                f.write("MAMIN_API_KEY=AIzaSyCOecBtlN7HEruezOrllhn8FNcCxbP-Mfs\n")
                f.write("OPENAI_API_KEY=\n")
            print("✅ Created basic .env file")
    else:
        print("✅ .env file already exists")
    return True

def check_tesseract():
    """Check if Tesseract OCR is installed"""
    print("\n🔍 Checking Tesseract OCR...")
    try:
        result = subprocess.run(['tesseract', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Tesseract OCR is installed")
            return True
        else:
            print("❌ Tesseract OCR not found")
            return False
    except FileNotFoundError:
        print("❌ Tesseract OCR not found")
        return False

def install_tesseract_instructions():
    """Provide instructions for installing Tesseract"""
    system = platform.system().lower()
    print(f"\n📋 Tesseract OCR Installation Instructions for {system}:")
    
    if system == "windows":
        print("1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Install the downloaded .exe file")
        print("3. Add Tesseract to your PATH environment variable")
        print("4. Restart your terminal/command prompt")
    elif system == "darwin":  # macOS
        print("Run: brew install tesseract")
    elif system == "linux":
        print("Run: sudo apt-get install tesseract-ocr")
    else:
        print("Please install Tesseract OCR for your operating system")

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🧪 Testing imports...")
    required_modules = [
        'cv2', 'PIL', 'numpy', 'matplotlib', 'sympy', 'scipy',
        'pytesseract', 'easyocr', 'moviepy', 'gtts', 'flask',
        'requests'
    ]
    
    failed_imports = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n⚠️  Failed to import: {', '.join(failed_imports)}")
        print("Please install missing dependencies with: pip install -r requirements.txt")
        return False
    
    print("✅ All required modules imported successfully")
    return True

def main():
    """Main setup function"""
    print("🚀 AI Math Problem Solver Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("⚠️  Some dependencies failed to install. Continuing...")
    
    # Create directories
    create_directories()
    
    # Setup environment
    setup_environment()
    
    # Check Tesseract
    if not check_tesseract():
        install_tesseract_instructions()
        print("⚠️  Please install Tesseract OCR before using the system")
    
    # Test imports
    if not test_imports():
        print("⚠️  Some modules failed to import. Please check your installation.")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Install Tesseract OCR if not already installed")
    print("2. Run: python test_system.py (to test the system)")
    print("3. Run: python app.py (to start the web server)")
    print("4. Open http://localhost:5000 in your browser")
    print("\nThe system is now configured with Mamin API integration!")

if __name__ == "__main__":
    main()
