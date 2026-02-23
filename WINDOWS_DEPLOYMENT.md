# Windows Deployment Notes

## ⚠️ Important: Gunicorn on Windows

**Gunicorn does NOT work on Windows.** It's a Unix-only WSGI server.

### For Local Development on Windows:

Use Django's development server:
```bash
python manage.py runserver
```

### For Production Deployment from Windows:

You have two options:

#### Option 1: Deploy to Linux-based Platform (Recommended)
Deploy to platforms that run Linux servers:
- **Railway** (easiest - auto-detects and uses gunicorn)
- **Render** (free tier available)
- **Heroku** (uses gunicorn automatically)
- **AWS Elastic Beanstalk** (Linux environment)
- **DigitalOcean App Platform**

These platforms will use gunicorn automatically when they detect your Django app.

#### Option 2: Use Windows-Compatible WSGI Server

If you must run on Windows server, replace gunicorn with waitress:

1. Update `requirements.txt`:
```
# Replace gunicorn with:
waitress==2.1.2
```

2. Create `run_waitress.py`:
```python
from waitress import serve
from config.wsgi import application

if __name__ == '__main__':
    serve(application, host='0.0.0.0', port=8000)
```

3. Run with:
```bash
python run_waitress.py
```

## ✅ Your Project is Ready for Deployment

All security fixes are applied. To deploy:

### Quick Deploy to Railway (Recommended):

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login and deploy:
```bash
cd backend
railway login
railway init
railway up
```

3. Add PostgreSQL:
```bash
railway add postgresql
```

4. Set environment variables in Railway dashboard:
   - SECRET_KEY (generate new one)
   - DEBUG=False
   - ALLOWED_HOSTS=your-app.railway.app
   - CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app

### Deploy Frontend to Vercel:

1. Update `frontend/.env.production`:
```
REACT_APP_API_URL=https://your-backend.railway.app/api
```

2. Build and deploy:
```bash
cd frontend
npm install
npm run build
npx vercel --prod
```

## Testing Locally

To test your secured settings locally:

```bash
# Backend
cd backend
python manage.py runserver

# Frontend (new terminal)
cd frontend
npm start
```

Everything should work as before, but now it's secure and production-ready!

## Environment Variables

Your `.env` file is already configured for local development:
- SECRET_KEY: ✅ Set
- DEBUG: ✅ True (for local dev)
- ALLOWED_HOSTS: ✅ localhost,127.0.0.1
- DATABASE_URL: ✅ SQLite (for local dev)
- CORS_ALLOWED_ORIGINS: ✅ localhost:3000

For production, you'll set these in your deployment platform's dashboard.
