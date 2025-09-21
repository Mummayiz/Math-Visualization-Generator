import React, { useState, useRef } from 'react';
import Head from 'next/head';

const API_BASE_URL = 'https://math-vis-backend-production.up.railway.app';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState('');
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');
  const [taskId, setTaskId] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError('');
      setResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setProgress(0);
    setMessage('Starting upload...');
    setError('');

    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.success) {
        setTaskId(data.task_id);
        setMessage('Upload successful! Processing...');
        pollProgress(data.task_id);
      } else {
        setError(data.error || 'Upload failed');
        setUploading(false);
      }
    } catch (err) {
      setError('Upload failed: ' + (err as Error).message);
      setUploading(false);
    }
  };

  const pollProgress = async (taskId: string) => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/progress/${taskId}`);
        const data = await response.json();

        setProgress(data.progress);
        setMessage(data.message);

        if (data.status === 'completed') {
          clearInterval(interval);
          setResult(data.result);
          setUploading(false);
          setMessage('Processing completed!');
        } else if (data.status === 'error') {
          clearInterval(interval);
          setError(data.message);
          setUploading(false);
        }
      } catch (err) {
        clearInterval(interval);
        setError('Progress check failed: ' + (err as Error).message);
        setUploading(false);
      }
    }, 1000);
  };

  const resetForm = () => {
    setFile(null);
    setUploading(false);
    setProgress(0);
    setMessage('');
    setResult(null);
    setError('');
    setTaskId(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <>
      <Head>
        <title>Math Visualization Generator</title>
        <meta name="description" content="Upload math problems and get step-by-step solutions" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="container">
        <div className="header">
          <h1>🧮 Math Visualization Generator</h1>
          <div className="badge">
            🚀 Frontend: Vercel | Backend: Railway
          </div>
        </div>

        <div className="upload-section">
          <div 
            className="upload-area"
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
            <div className="upload-icon">📁</div>
            <h3>Upload Math Problem Image</h3>
            <p>Click here or drag & drop your image</p>
            {file && (
              <div className="file-info">
                <strong>Selected:</strong> {file.name}
              </div>
            )}
          </div>

          <div className="button-group">
            <button 
              className="btn btn-primary" 
              onClick={handleUpload}
              disabled={!file || uploading}
            >
              {uploading ? 'Processing...' : 'Upload & Solve'}
            </button>
            <button 
              className="btn btn-secondary" 
              onClick={resetForm}
              disabled={uploading}
            >
              Reset
            </button>
          </div>
        </div>

        {uploading && (
          <div className="progress-section">
            <h3>Processing your problem...</h3>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${progress}%` }}
              >
                {progress}%
              </div>
            </div>
            <p className="progress-message">{message}</p>
          </div>
        )}

        {result && (
          <div className="result-section">
            <h3>✅ Solution Found!</h3>
            <div className="result-content">
              <p><strong>Problem:</strong> {result.problem}</p>
              <p><strong>Answer:</strong> {result.answer}</p>
              <div className="steps">
                <h4>Solution Steps:</h4>
                <ol>
                  {result.steps?.map((step: string, index: number) => (
                    <li key={index}>{step}</li>
                  ))}
                </ol>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="error-section">
            <h3>❌ Error</h3>
            <p>{error}</p>
          </div>
        )}

        <div className="info-section">
          <h3>How it works:</h3>
          <ol>
            <li><strong>Frontend (Vercel):</strong> Handles the UI and file upload</li>
            <li><strong>Backend (Railway):</strong> Processes the image with OCR and AI</li>
            <li><strong>Real-time:</strong> Progress updates and results display</li>
          </ol>
        </div>
      </div>

      <style jsx>{`
        .container {
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        .header {
          text-align: center;
          margin-bottom: 30px;
        }

        .header h1 {
          color: #2c3e50;
          margin-bottom: 10px;
        }

        .badge {
          background: linear-gradient(45deg, #000, #333);
          color: white;
          padding: 8px 16px;
          border-radius: 20px;
          font-size: 14px;
          display: inline-block;
        }

        .upload-section {
          margin-bottom: 30px;
        }

        .upload-area {
          border: 2px dashed #28a745;
          border-radius: 10px;
          padding: 40px;
          text-align: center;
          cursor: pointer;
          transition: all 0.3s ease;
          margin-bottom: 20px;
        }

        .upload-area:hover {
          background-color: #e6f7ee;
          border-color: #218838;
        }

        .upload-icon {
          font-size: 48px;
          margin-bottom: 15px;
        }

        .file-info {
          margin-top: 15px;
          padding: 10px;
          background: #f8f9fa;
          border-radius: 5px;
          color: #495057;
        }

        .button-group {
          display: flex;
          gap: 15px;
          justify-content: center;
        }

        .btn {
          padding: 12px 25px;
          border: none;
          border-radius: 5px;
          cursor: pointer;
          font-size: 16px;
          font-weight: 600;
          transition: all 0.3s ease;
        }

        .btn-primary {
          background: #28a745;
          color: white;
        }

        .btn-primary:hover:not(:disabled) {
          background: #218838;
          transform: translateY(-2px);
        }

        .btn-primary:disabled {
          background: #6c757d;
          cursor: not-allowed;
        }

        .btn-secondary {
          background: #6c757d;
          color: white;
        }

        .btn-secondary:hover:not(:disabled) {
          background: #5a6268;
          transform: translateY(-2px);
        }

        .progress-section {
          margin: 30px 0;
          padding: 20px;
          background: #f8f9fa;
          border-radius: 10px;
          text-align: center;
        }

        .progress-bar {
          width: 100%;
          height: 25px;
          background: #e0e0e0;
          border-radius: 5px;
          overflow: hidden;
          margin: 15px 0;
        }

        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, #28a745, #20c997);
          transition: width 0.5s ease;
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-weight: bold;
        }

        .progress-message {
          color: #495057;
          font-style: italic;
        }

        .result-section {
          margin: 30px 0;
          padding: 20px;
          background: #e9f7ef;
          border: 1px solid #28a745;
          border-radius: 10px;
        }

        .result-content {
          margin-top: 15px;
        }

        .steps {
          margin-top: 15px;
        }

        .steps ol {
          padding-left: 20px;
        }

        .steps li {
          margin-bottom: 8px;
          line-height: 1.5;
        }

        .error-section {
          margin: 30px 0;
          padding: 20px;
          background: #f8d7da;
          border: 1px solid #f5c6cb;
          border-radius: 10px;
          color: #721c24;
        }

        .info-section {
          margin: 30px 0;
          padding: 20px;
          background: #e3f2fd;
          border-radius: 10px;
        }

        .info-section ol {
          padding-left: 20px;
        }

        .info-section li {
          margin-bottom: 10px;
          line-height: 1.5;
        }
      `}</style>
    </>
  );
}
