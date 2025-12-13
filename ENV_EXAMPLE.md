# Backend Environment Variables

Copy this file to `.env` for local development. For production, set these in Railway.

```bash
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here-change-in-production
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for local development, production uses Railway Postgres)
# POSTGRES_DB=postgres
# POSTGRES_USER=postgres
# POSTGRES_PASSWORD=your-password
# POSTGRES_HOST=localhost
# POSTGRES_PORT=5432

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.vercel.app
CSRF_TRUSTED_ORIGINS=https://your-backend-domain.railway.app,https://your-frontend-domain.vercel.app

# CPX Research Integration
CPX_APP_ID=your-cpx-app-id
CPX_SECURITY_HASH=your-cpx-security-hash
CPX_CURRENCY_FACTOR=1000
CPX_SECRET=your-cpx-secret
CPX_REQUIRE_SECURE_HASH=false

# Security (for production)
SECURE_SSL_REDIRECT=True
```

