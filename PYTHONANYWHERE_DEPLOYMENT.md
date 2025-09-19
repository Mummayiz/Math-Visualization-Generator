# PythonAnywhere Deployment Guide

This guide will walk you through deploying the Math Visualization Generator to PythonAnywhere.

## Prerequisites
- A PythonAnywhere account (free tier available)
- Your Math-Visualization-Generator repository

## Step 1: Create a PythonAnywhere Account
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Click "Sign up for a free account"
3. Choose the "Beginner" plan (free)
4. Complete the registration

## Step 2: Upload Your Code
1. Once logged in, go to the "Files" tab
2. Navigate to `/home/yourusername/`
3. Create a new directory: `mkdir math-visualization`
4. Upload your files:
   - `pythonanywhere_app.py` (main app file)
   - `templates/pythonanywhere_index.html` (HTML template)
   - `requirements.txt` (dependencies)

## Step 3: Install Dependencies
1. Go to the "Consoles" tab
2. Start a new Bash console
3. Navigate to your project: `cd math-visualization`
4. Install dependencies:
   ```bash
   pip3.10 install --user flask flask-cors werkzeug
   ```

## Step 4: Configure Web App
1. Go to the "Web" tab
2. Click "Add a new web app"
3. Choose "Flask"
4. Select Python 3.10
5. Set the source code directory to `/home/yourusername/math-visualization`
6. Set the WSGI file to `/home/yourusername/math-visualization/pythonanywhere_app.py`

## Step 5: Configure WSGI File
1. Click on the WSGI configuration file link
2. Replace the content with:
   ```python
   import sys
   path = '/home/yourusername/math-visualization'
   if path not in sys.path:
       sys.path.append(path)
   
   from pythonanywhere_app import app as application
   ```

## Step 6: Reload Web App
1. Go back to the "Web" tab
2. Click "Reload" to restart your web app
3. Your app should now be live at `yourusername.pythonanywhere.com`

## Step 7: Test Your App
1. Visit your app URL
2. Test the health check: `yourusername.pythonanywhere.com/health`
3. Test the main page: `yourusername.pythonanywhere.com`
4. Try uploading an image

## Troubleshooting

### If the app doesn't load:
1. Check the error log in the "Web" tab
2. Make sure all files are uploaded correctly
3. Verify the WSGI configuration

### If dependencies are missing:
1. Install them in the console:
   ```bash
   pip3.10 install --user flask flask-cors werkzeug
   ```

### If you get permission errors:
1. Make sure files are in the correct directory
2. Check file permissions

## Features Available
- ✅ File upload
- ✅ Progress tracking
- ✅ Math problem display
- ✅ Step-by-step solutions
- ✅ History functionality
- ✅ Responsive design

## Next Steps
Once the basic app is working, you can gradually add back:
1. Real OCR functionality
2. Real math solving
3. Video generation
4. AI integration

## Support
- PythonAnywhere documentation: https://help.pythonanywhere.com/
- Community forum: https://www.pythonanywhere.com/forums/
