# 🚀 Render.com Environment Variables Template

Copy these environment variables to your Render.com service's Environment Variables section.
**Replace the placeholder values with your actual credentials.**

## 🔐 APPLICATION SETTINGS
```
ENVIRONMENT=production
DEBUG=false
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=info
```

## 🔑 SECURE PRODUCTION KEYS (Generated)
```
JWT_SECRET_KEY=-4dr0hnXwD7IWPHE5Y9Q87GyqRcrLUzB9kAXiIdqaN-vskKZX1bagrkLhee7MNfi
SECRET_KEY=dFAd83-kGmonpNAD9mLUD67dd7phQMJe1w52jc6TqjHlfMekaUwhKAth4CPOSsvp
SESSION_SECRET_KEY=m5VPHCKbKKsv_JP0kjQe-V29BdCVR220_SLfLMVS9nlURUvX-L8HddviGS62GJG-
PASSWORD_SALT=ghlM7oNeN2CXx8uOfqP8Gou0ucN_3kb8
```

## 🔐 JWT AUTHENTICATION CONFIG
```
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

## 📱 SESSION CONFIG
```
PASSWORD_HASH_ALGORITHM=bcrypt
PASSWORD_HASH_ROUNDS=12
SESSION_MAX_AGE=3600
SESSION_COOKIE_NAME=agent_makalah_session
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true
SESSION_COOKIE_SAMESITE=lax
```

## 🗄️ SUPABASE CREDENTIALS (Your actual values)
```
SUPABASE_URL=https://pjzzwlethszhjyzxgjmd.supabase.co
SUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY=YOUR_SUPABASE_SERVICE_ROLE_KEY
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.pjzzwlethszhjyzxgjmd.supabase.co:5432/postgres
SUPABASE_PROJECT_REF=pjzzwlethszhjyzxgjmd
SUPABASE_PROJECT_ID=pjzzwlethszhjyzxgjmd
SUPABASE_JWT_SECRET=YOUR_SUPABASE_JWT_SECRET
```

## 🐘 DATABASE COMPONENTS
```
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=YOUR_POSTGRES_PASSWORD
POSTGRES_HOST=db.pjzzwlethszhjyzxgjmd.supabase.co
POSTGRES_PORT=5432
```

## 📦 STORAGE
```
SUPABASE_STORAGE_URL=https://pjzzwlethszhjyzxgjmd.supabase.co/storage/v1
S3_ENDPOINT=https://pjzzwlethszhjyzxgjmd.supabase.co/storage/v1/s3
```

## 🔴 REDIS CONFIGURATION
```
UPSTASH_REDIS_URL=https://growing-fly-25129.upstash.io
UPSTASH_REDIS_TOKEN=YOUR_UPSTASH_REDIS_TOKEN
REDIS_URL=https://growing-fly-25129.upstash.io
```

## 🤖 AI/LLM PROVIDER KEYS
```
OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE
```

## 🌐 CORS & SECURITY (Production)
```
CORS_ORIGINS=["https://makalah.ai","https://www.makalah.ai","https://api.makalah.ai"]
ALLOWED_HOSTS=["makalah.ai","www.makalah.ai","api.makalah.ai","localhost","127.0.0.1"]
```

## 📄 FILE UPLOAD CONFIGURATION
```
MAX_FILE_SIZE_MB=50
ALLOWED_FILE_TYPES=["pdf","docx","txt"]
UPLOAD_DIR=uploads
```

## 🤖 AGENT SYSTEM CONFIGURATION
```
MAX_CONCURRENT_AGENTS=6
AGENT_TIMEOUT_SECONDS=300
SESSION_TIMEOUT_MINUTES=60
```

## 📝 ACADEMIC WRITING CONFIGURATION
```
DEFAULT_LANGUAGE=id
MAX_PAPER_LENGTH_WORDS=10000
MAX_REVISION_CYCLES=3
```

---

## 📋 Deployment Checklist

1. ✅ Create new Web Service on Render.com
2. ✅ Connect GitHub repository: `makalah-app/makalah-agent`
3. ✅ Set Runtime: `Docker`
4. ✅ Build Command: (use Dockerfile)
5. ✅ Start Command: (defined in Dockerfile)
6. ✅ Copy all environment variables above
7. ✅ Deploy and test endpoints

## 🔗 Expected Endpoints After Deployment

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /auth/register` - User registration
- `POST /auth/login` - User authentication
- `POST /auth/logout` - User logout
- `GET /auth/profile` - Get user profile
- `GET /docs` - API documentation

---

**⚠️ Security Note**: Never commit actual API keys to version control! Use Render.com's Environment Variables section for all sensitive credentials. 