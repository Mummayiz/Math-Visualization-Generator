# Vercel + Railway Deployment Guide

This guide will help you deploy the Math Visualization Generator using Vercel for frontend and Railway for backend.

## Architecture Overview

```
Frontend (Vercel)          Backend (Railway)
┌─────────────────┐       ┌─────────────────┐
│   Next.js App   │  ──►  │   Python API    │
│   - React UI    │       │   - Real OCR    │
│   - File Upload │       │   - Math Solve  │
│   - Progress    │       │   - Video Gen   │
│   - Results     │       │   - CORS enabled│
└─────────────────┘       └─────────────────┘
```

## Part 1: Deploy Backend to Railway

### Step 1: Prepare Backend Repository
1. Create a new GitHub repository for the backend
2. Upload the `backend/` folder contents to the new repository
3. Make sure these files are included:
   - `api_app.py`
   - `real_ocr.py`
   - `real_math_solver.py`
   - `requirements.txt`
   - `Procfile`
   - `railway.json`

### Step 2: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your backend repository
5. Railway will automatically detect Python and deploy
6. Wait for deployment to complete
7. Note your Railway app URL (e.g., `https://your-app.railway.app`)

### Step 3: Test Backend
1. Visit your Railway app URL
2. Test health check: `https://your-app.railway.app/health`
3. Should return: `{"status": "healthy", "message": "Math Visualization Generator API is running on Railway"}`

## Part 2: Deploy Frontend to Vercel

### Step 1: Prepare Frontend Repository
1. Create a new GitHub repository for the frontend
2. Upload the `frontend/` folder contents to the new repository
3. Make sure these files are included:
   - `pages/index.tsx`
   - `package.json`
   - `next.config.js`
   - `vercel.json`
   - `env.example`

### Step 2: Deploy to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your frontend repository
4. Vercel will automatically detect Next.js
5. Add environment variable:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: Your Railway backend URL (e.g., `https://your-app.railway.app`)
6. Click "Deploy"
7. Wait for deployment to complete

### Step 3: Test Frontend
1. Visit your Vercel app URL
2. You should see the Math Visualization Generator interface
3. Try uploading an image to test the full flow

## Part 3: Configure CORS (Important!)

### Backend CORS Configuration
The backend already has CORS enabled for all origins:
```python
from flask_cors import CORS
CORS(app)  # This allows all origins
```

### If you need to restrict CORS:
```python
CORS(app, origins=["https://your-vercel-app.vercel.app"])
```

## Part 4: Test the Full System

### Test Flow:
1. **Frontend (Vercel):** Upload a math problem image
2. **Backend (Railway):** Receives image, processes with OCR
3. **Backend (Railway):** Solves the math problem
4. **Frontend (Vercel):** Displays results with progress tracking

### Expected Features:
- ✅ **Real OCR** - Extracts text from images
- ✅ **Real Math Solving** - Solves various problem types
- ✅ **Progress Tracking** - Real-time updates
- ✅ **Step-by-Step Solutions** - Detailed solving process
- ✅ **Responsive UI** - Works on all devices

## Troubleshooting

### Backend Issues:
1. **Health check fails:** Check Railway logs
2. **OCR not working:** Verify Tesseract installation
3. **CORS errors:** Check CORS configuration

### Frontend Issues:
1. **API connection fails:** Verify `NEXT_PUBLIC_API_URL`
2. **Upload not working:** Check file size limits
3. **Progress not updating:** Check polling interval

### Common Solutions:
1. **Check logs:** Both Vercel and Railway provide detailed logs
2. **Verify URLs:** Make sure frontend points to correct backend
3. **Test endpoints:** Use curl or Postman to test API directly

## Environment Variables

### Backend (Railway):
- `FLASK_ENV=production`
- `PORT=8000`

### Frontend (Vercel):
- `NEXT_PUBLIC_API_URL=https://your-railway-app.railway.app`

## Cost Breakdown

### Vercel:
- **Free tier:** 100GB bandwidth, unlimited deployments
- **Pro tier:** $20/month (if needed)

### Railway:
- **Free tier:** $5 credit monthly
- **Pro tier:** $20/month (recommended for production)

### Total Cost:
- **Free:** $0 (using free tiers)
- **Production:** $20-40/month (both platforms)

## Benefits of This Architecture

1. **Performance:** Vercel's CDN makes frontend super fast
2. **Scalability:** Railway handles backend processing well
3. **Reliability:** Both platforms are very stable
4. **Development:** Easy to update and deploy
5. **Cost:** Reasonable pricing for production use

## Next Steps

1. **Deploy both parts** following this guide
2. **Test thoroughly** with different math problems
3. **Add more features** like video generation
4. **Optimize performance** based on usage
5. **Monitor and maintain** both deployments

## Support

- **Vercel Docs:** https://vercel.com/docs
- **Railway Docs:** https://docs.railway.app
- **GitHub Issues:** Create issues in your repositories
