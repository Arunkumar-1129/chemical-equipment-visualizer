# Render Deployment Guide

## 🚀 Deploy Backend to Render

### Method 1: Using Render Dashboard (Easiest)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Create Web Service on Render**
   - Go to https://dashboard.render.com/
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure Web Service**
   ```
   Name: equipment-visualizer-backend
   Region: Oregon (or closest to you)
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: ./build.sh
   Start Command: gunicorn config.wsgi:application
   ```

4. **Add Environment Variables**
   Click "Advanced" → "Add Environment Variable":
   
   ```
   SECRET_KEY = [Click "Generate" to auto-generate]
   DEBUG = False
   ALLOWED_HOSTS = your-app-name.onrender.com
   CORS_ALLOWED_ORIGINS = https://your-frontend-url.vercel.app
   ```

5. **Add PostgreSQL Database**
   - In Render Dashboard, click "New +" → "PostgreSQL"
   - Name: equipment-visualizer-db
   - After creation, copy the "Internal Database URL"
   - Add to your web service environment variables:
   ```
   DATABASE_URL = [paste Internal Database URL]
   ```

6. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy
   - Wait 5-10 minutes for first deployment

### Method 2: Using render.yaml (Infrastructure as Code)

1. **Push to GitHub** (with render.yaml included)
   ```bash
   git add .
   git commit -m "Add Render configuration"
   git push origin main
   ```

2. **Create Blueprint on Render**
   - Go to https://dashboard.render.com/
   - Click "New +" → "Blueprint"
   - Connect your repository
   - Render will detect render.yaml and set everything up

3. **Set Required Environment Variables**
   After blueprint creation, go to your web service and add:
   ```
   ALLOWED_HOSTS = your-app-name.onrender.com
   CORS_ALLOWED_ORIGINS = https://your-frontend-url.vercel.app
   ```

## 🎨 Deploy Frontend to Vercel

1. **Update Frontend Environment**
   
   Edit `frontend/.env.production`:
   ```
   REACT_APP_API_URL=https://your-backend-name.onrender.com/api
   ```

2. **Deploy to Vercel**
   ```bash
   cd frontend
   npm install -g vercel
   vercel login
   vercel --prod
   ```

   Or use Vercel Dashboard:
   - Go to https://vercel.com/
   - Import your GitHub repository
   - Root Directory: `frontend`
   - Framework Preset: Create React App
   - Add Environment Variable:
     ```
     REACT_APP_API_URL = https://your-backend-name.onrender.com/api
     ```

## 📋 Post-Deployment Checklist

After deployment:

1. **Create Superuser** (via Render Shell)
   - Go to your web service on Render
   - Click "Shell" tab
   - Run:
   ```bash
   python manage.py createsuperuser
   ```

2. **Update CORS Settings**
   - Get your Vercel frontend URL
   - Update `CORS_ALLOWED_ORIGINS` in Render environment variables
   - Example: `https://your-app.vercel.app`

3. **Update ALLOWED_HOSTS**
   - Add your Render backend URL
   - Example: `your-backend.onrender.com`

4. **Test Your Deployment**
   - Visit your frontend URL
   - Try registering/logging in
   - Upload a CSV file
   - Check if data displays correctly

## 🔧 Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Ensure `build.sh` has execute permissions
- Verify all dependencies in requirements.txt

### Static Files Not Loading
- Check if `collectstatic` ran in build logs
- Verify STATIC_ROOT and STATIC_URL in settings.py
- Whitenoise should handle this automatically

### Database Connection Error
- Verify DATABASE_URL is set correctly
- Use "Internal Database URL" from Render PostgreSQL
- Check if migrations ran successfully

### CORS Errors
- Verify CORS_ALLOWED_ORIGINS includes your frontend URL
- Must use HTTPS in production (not HTTP)
- Check browser console for exact error

### 502 Bad Gateway
- Check application logs in Render
- Verify gunicorn is starting correctly
- Check if migrations completed

## 💰 Render Free Tier Limits

- Web Services: Spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 750 hours/month free
- PostgreSQL: 90 days free, then $7/month

## 🔄 Continuous Deployment

Render auto-deploys when you push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

## 📊 Monitoring

- View logs: Render Dashboard → Your Service → Logs
- Check metrics: Dashboard → Your Service → Metrics
- Set up alerts: Dashboard → Your Service → Settings → Notifications

## 🔗 Useful Links

- Render Dashboard: https://dashboard.render.com/
- Render Docs: https://render.com/docs
- Your Backend URL: https://your-app-name.onrender.com
- Your Frontend URL: https://your-app.vercel.app

## ⚡ Quick Commands

```bash
# View logs
render logs -s your-service-name

# Open shell
render shell -s your-service-name

# Restart service
render restart -s your-service-name
```

---

Your app is ready to deploy! 🎉
