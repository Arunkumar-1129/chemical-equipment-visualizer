# 🚀 RENDER DEPLOYMENT - QUICK START

## Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

## Step 2: Deploy Backend on Render

1. Go to https://dashboard.render.com/
2. Click "New +" → "Web Service"
3. Connect GitHub → Select your repo
4. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application`

5. Add Environment Variables:
   ```
   SECRET_KEY = [Generate new one]
   DEBUG = False
   ALLOWED_HOSTS = your-app.onrender.com
   CORS_ALLOWED_ORIGINS = https://your-frontend.vercel.app
   ```

6. Add PostgreSQL:
   - New + → PostgreSQL
   - Copy "Internal Database URL"
   - Add to web service: `DATABASE_URL = [paste URL]`

7. Click "Create Web Service"

## Step 3: Deploy Frontend on Vercel

1. Update `frontend/.env.production`:
   ```
   REACT_APP_API_URL=https://your-backend.onrender.com/api
   ```

2. Deploy:
   ```bash
   cd frontend
   npx vercel --prod
   ```

## Step 4: Update CORS

After getting Vercel URL, update Render environment variable:
```
CORS_ALLOWED_ORIGINS = https://your-app.vercel.app
```

## Done! 🎉

- Backend: https://your-app.onrender.com
- Frontend: https://your-app.vercel.app

See RENDER_DEPLOYMENT.md for detailed instructions.
