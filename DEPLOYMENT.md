# Deployment Guide

## Security Fixes Applied ✅

1. ✅ SECRET_KEY moved to environment variables
2. ✅ DEBUG controlled by environment variable (False by default)
3. ✅ ALLOWED_HOSTS restricted and configurable
4. ✅ CORS_ALLOW_ALL_ORIGINS only enabled in development
5. ✅ Added security headers for production
6. ✅ Added whitenoise for static file serving
7. ✅ Database URL configuration for PostgreSQL support
8. ✅ SSL/HTTPS enforcement in production

## Environment Variables Required

Create a `.env` file in the backend directory with:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:password@host:port/dbname
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Generate Secret Key

Run this Python command to generate a secure secret key:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Deployment Options

### Option 1: Railway (Recommended - Easy)

1. Install Railway CLI or use web interface
2. Create new project: `railway init`
3. Add PostgreSQL: `railway add postgresql`
4. Set environment variables in Railway dashboard
5. Deploy: `railway up`

### Option 2: Render

1. Create new Web Service
2. Connect your GitHub repository
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn config.wsgi:application`
5. Add PostgreSQL database
6. Set environment variables in dashboard

### Option 3: Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Add PostgreSQL: `heroku addons:create heroku-postgresql:mini`
5. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```
6. Deploy: `git push heroku main`

### Option 4: AWS Elastic Beanstalk

1. Install EB CLI: `pip install awsebcli`
2. Initialize: `eb init -p python-3.11 your-app-name`
3. Create environment: `eb create production-env`
4. Set environment variables: `eb setenv SECRET_KEY=xxx DEBUG=False`
5. Deploy: `eb deploy`

## Frontend Deployment

### Update Frontend Environment

Create `.env.production` in frontend directory:

```env
REACT_APP_API_URL=https://your-backend-domain.com/api
```

### Build Frontend

```bash
cd frontend
npm install
npm run build
```

### Deploy Frontend Options

1. **Vercel** (Recommended for React)
   - Connect GitHub repository
   - Auto-deploys on push
   - Set environment variable: `REACT_APP_API_URL`

2. **Netlify**
   - Drag and drop `build` folder
   - Or connect GitHub repository
   - Set environment variable in dashboard

3. **AWS S3 + CloudFront**
   - Upload build folder to S3
   - Configure CloudFront distribution
   - Set up custom domain

## Pre-Deployment Checklist

- [ ] Generate new SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up PostgreSQL database
- [ ] Configure CORS_ALLOWED_ORIGINS
- [ ] Update frontend API URL
- [ ] Run migrations: `python manage.py migrate`
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Test in production mode locally

## Local Production Testing

Test production settings locally:

```bash
# Backend
cd backend
export DEBUG=False
export SECRET_KEY=test-key
python manage.py collectstatic --noinput
gunicorn config.wsgi:application

# Frontend
cd frontend
npm run build
npx serve -s build
```

## Database Migration

If moving from SQLite to PostgreSQL:

```bash
# Dump data from SQLite
python manage.py dumpdata > data.json

# Update DATABASE_URL to PostgreSQL
# Run migrations
python manage.py migrate

# Load data
python manage.py loaddata data.json
```

## Monitoring & Maintenance

- Set up error tracking (Sentry)
- Configure logging
- Set up database backups
- Monitor application performance
- Keep dependencies updated

## Troubleshooting

### Static files not loading
- Run: `python manage.py collectstatic`
- Check STATIC_ROOT and STATIC_URL settings

### CORS errors
- Verify CORS_ALLOWED_ORIGINS includes your frontend domain
- Check protocol (http vs https)

### Database connection errors
- Verify DATABASE_URL format
- Check database credentials
- Ensure database is accessible from deployment server

## Support

For issues, check:
- Django deployment docs: https://docs.djangoproject.com/en/4.2/howto/deployment/
- Platform-specific documentation
- Application logs
