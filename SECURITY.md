# Security Checklist

## ✅ Completed Security Fixes

- [x] SECRET_KEY moved to environment variables
- [x] DEBUG set to False by default in production
- [x] ALLOWED_HOSTS restricted and configurable
- [x] CORS_ALLOW_ALL_ORIGINS disabled in production
- [x] Added security middleware (whitenoise)
- [x] Database URL configuration for production databases
- [x] SSL/HTTPS enforcement in production
- [x] Secure cookie settings (SECURE, HTTPONLY)
- [x] XSS protection enabled
- [x] Content type sniffing protection
- [x] Clickjacking protection (X-Frame-Options)
- [x] HSTS headers configured
- [x] Static files properly configured with whitenoise

## 🔒 Before Deployment

### Critical
- [ ] Generate new SECRET_KEY (run: `python backend/generate_secret_key.py`)
- [ ] Set DEBUG=False in production .env
- [ ] Configure ALLOWED_HOSTS with your domain
- [ ] Set up PostgreSQL database (recommended for production)
- [ ] Update CORS_ALLOWED_ORIGINS with your frontend domain
- [ ] Update frontend .env.production with backend API URL

### Recommended
- [ ] Set up SSL certificate (Let's Encrypt or platform-provided)
- [ ] Configure database backups
- [ ] Set up error monitoring (Sentry, Rollbar)
- [ ] Configure logging
- [ ] Set up CDN for static files (optional)
- [ ] Enable rate limiting for API endpoints
- [ ] Review and test all API endpoints
- [ ] Create superuser account
- [ ] Test file upload limits

### Optional but Good Practice
- [ ] Set up CI/CD pipeline
- [ ] Configure automated testing
- [ ] Set up staging environment
- [ ] Document API endpoints
- [ ] Add API versioning
- [ ] Implement request throttling
- [ ] Add health check endpoint
- [ ] Configure monitoring and alerts

## 🚨 Never Commit

- `.env` files with real credentials
- `db.sqlite3` database file
- `SECRET_KEY` values
- API keys or tokens
- Database passwords
- Any PII or sensitive data

## 🔍 Security Testing

Before going live:

1. Test with DEBUG=False locally
2. Verify HTTPS redirects work
3. Check CORS configuration
4. Test authentication flows
5. Verify file upload restrictions
6. Check rate limiting
7. Test error handling (don't expose stack traces)
8. Verify database connection security

## 📝 Environment Variables Reference

### Backend (.env)
```
SECRET_KEY=<50-char-random-string>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:pass@host:port/db
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### Frontend (.env.production)
```
REACT_APP_API_URL=https://api.yourdomain.com/api
```

## 🛡️ Additional Security Recommendations

1. **Database**: Use PostgreSQL instead of SQLite in production
2. **Passwords**: Ensure strong password policies
3. **File Uploads**: Validate file types and sizes
4. **API**: Implement rate limiting and throttling
5. **Monitoring**: Set up logging and error tracking
6. **Backups**: Regular automated database backups
7. **Updates**: Keep dependencies updated regularly
8. **Access**: Use principle of least privilege
9. **Secrets**: Use platform secret management (AWS Secrets Manager, etc.)
10. **Audit**: Regular security audits and penetration testing

## 📚 Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security](https://docs.djangoproject.com/en/4.2/topics/security/)
