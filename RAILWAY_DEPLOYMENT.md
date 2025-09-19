# Railway Deployment Guide

## Quick Setup (5 minutes)

### 1. Create Railway Account
- Go to [railway.app](https://railway.app)
- Sign up with GitHub
- Connect your GitHub account

### 2. Deploy Your App
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose "Math-Visualization-Generator"
- Railway will auto-detect Python app

### 3. Configure Environment Variables
Railway will automatically set:
- `PORT` (Railway assigns this)
- `FLASK_ENV=production`

### 4. Deploy
- Click "Deploy"
- Wait 2-3 minutes for build
- Your app will be live!

## Expected Results

### ✅ What Should Work:
- **App starts successfully** (no memory issues)
- **EasyOCR loads** on first request
- **OCR extraction** works perfectly
- **Video generation** works
- **No sleep issues** (always responsive)

### 📊 Performance:
- **Startup time:** 10-15 seconds (first time)
- **Memory usage:** 400-600MB (well within limits)
- **Cost:** $5-8/month (vs $25 on Render)
- **Reliability:** 99%+ uptime

## Troubleshooting

### If Build Fails:
- Check Railway logs
- Ensure all dependencies in requirements.txt
- Verify Python version compatibility

### If App Crashes:
- Check memory usage in Railway dashboard
- Look for EasyOCR initialization errors
- Verify all environment variables

## Cost Estimation

### Railway Pro Plan:
- **Base cost:** $5/month
- **Usage cost:** ~$2-3/month (for your app)
- **Total:** ~$7-8/month

### vs Render Standard:
- **Render Standard:** $25/month
- **Savings:** ~$17-18/month (70% cheaper!)

## Support

If you need help:
1. Check Railway logs
2. Test locally first
3. Contact Railway support
4. Check this guide

## Next Steps

1. Deploy to Railway
2. Test with math images
3. Compare with Render
4. Choose the better platform
5. Optimize as needed
