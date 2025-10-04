# StaffRoom - Free Hosting Deployment Guide

## 🌟 Free Hosting Options for StaffRoom

### 1. **Render.com** (Recommended)
- **Free Tier**: 750 hours/month (enough for personal use)
- **Features**: Automatic deployments from GitHub, custom domains, SSL certificates
- **Database**: PostgreSQL (free tier available)
- **Pros**: Easy setup, reliable, good documentation
- **Cons**: Sleeps after 15 minutes of inactivity (wakes up on first request)

### 2. **Railway.app**
- **Free Tier**: $5 credit monthly (usually enough for small apps)
- **Features**: GitHub integration, automatic deployments, custom domains
- **Database**: PostgreSQL, MySQL, Redis available
- **Pros**: Fast, modern platform, good performance
- **Cons**: Credit-based system

### 3. **Heroku** (Limited Free Tier)
- **Free Tier**: Discontinued, but has low-cost options ($5-7/month)
- **Features**: Easy deployment, add-ons marketplace
- **Database**: PostgreSQL add-on
- **Pros**: Mature platform, extensive documentation
- **Cons**: No longer free

### 4. **PythonAnywhere**
- **Free Tier**: Limited web apps, basic account
- **Features**: Python-focused, easy setup
- **Database**: MySQL, PostgreSQL
- **Pros**: Python-optimized, simple interface
- **Cons**: Limited resources on free tier

### 5. **Fly.io**
- **Free Tier**: 3 small VMs, 160GB bandwidth
- **Features**: Global deployment, Docker-based
- **Database**: PostgreSQL available
- **Pros**: Global edge deployment, good performance
- **Cons**: More complex setup

## 🚀 Recommended Deployment: Render.com

### Why Render.com?
1. **Truly Free**: 750 hours/month is sufficient for most use cases
2. **Easy Setup**: Connect GitHub repo and deploy automatically
3. **Database Included**: Free PostgreSQL database
4. **Custom Domain**: Free SSL certificates
5. **Reliable**: Good uptime and performance

## 📋 Pre-Deployment Checklist

### 1. Database Migration
- [ ] Convert SQLite to PostgreSQL
- [ ] Update database connection strings
- [ ] Test database operations

### 2. Environment Variables
- [ ] Set up environment variables for production
- [ ] Secure sensitive data (API keys, secrets)
- [ ] Configure database URLs

### 3. Static Files
- [ ] Configure static file serving
- [ ] Set up file upload handling
- [ ] Test file operations

### 4. Security
- [ ] Enable HTTPS
- [ ] Set secure session cookies
- [ ] Configure CORS if needed

## 🛠️ Deployment Steps for Render.com

### Step 1: Prepare Your Code
```bash
# Create requirements.txt for production
pip freeze > requirements.txt

# Create render.yaml for configuration
# Create Procfile for process management
```

### Step 2: Database Setup
```python
# Update web_app.py for PostgreSQL
import os
from sqlalchemy import create_engine

# Use environment variable for database URL
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///teacher_app.db')

# For PostgreSQL on Render
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
```

### Step 3: Environment Variables
```bash
# Set in Render dashboard
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### Step 4: Deploy
1. Push code to GitHub
2. Connect GitHub repo to Render
3. Configure build and start commands
4. Set environment variables
5. Deploy!

## 💰 Cost Breakdown

### Render.com (Recommended)
- **Web Service**: Free (750 hours/month)
- **PostgreSQL Database**: Free (1GB storage)
- **Custom Domain**: Free
- **SSL Certificate**: Free
- **Total**: $0/month

### Railway.app
- **Web Service**: $5 credit/month (usually sufficient)
- **PostgreSQL**: Included in credit
- **Custom Domain**: Free
- **Total**: ~$0-5/month

## 🔧 Required Code Changes

### 1. Database Configuration
```python
# web_app.py
import os
from sqlalchemy import create_engine

def get_database_url():
    """Get database URL from environment or use SQLite fallback"""
    if 'DATABASE_URL' in os.environ:
        url = os.environ['DATABASE_URL']
        # Fix for older PostgreSQL URLs
        if url.startswith('postgres://'):
            url = url.replace('postgres://', 'postgresql://', 1)
        return url
    return 'sqlite:///teacher_app.db'
```

### 2. Production Settings
```python
# web_app.py
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key'),
    UPLOAD_FOLDER=os.environ.get('UPLOAD_FOLDER', 'uploads'),
    MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 16MB max file size
)

# Disable debug mode in production
if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

### 3. Static File Handling
```python
# For production static file serving
from flask import send_from_directory

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
```

## 📁 Required Files for Deployment

### 1. requirements.txt
```
Flask==2.3.3
Werkzeug==2.3.7
SQLAlchemy==2.0.21
psycopg2-binary==2.9.7
python-dotenv==1.0.0
```

### 2. Procfile
```
web: python web_app.py
```

### 3. render.yaml
```yaml
services:
  - type: web
    name: staffroom
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python web_app.py
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
  - type: pserv
    name: staffroom-db
    env: postgresql
```

## 🎯 Next Steps

1. **Choose Hosting Platform**: Render.com recommended
2. **Prepare Code**: Make necessary changes for production
3. **Set Up Database**: Convert to PostgreSQL
4. **Deploy**: Follow platform-specific instructions
5. **Test**: Verify all features work in production
6. **Custom Domain**: Set up your own domain (optional)

## 📞 Support

If you need help with deployment, I can:
1. Help modify the code for production
2. Guide you through the deployment process
3. Troubleshoot any issues
4. Optimize for performance

Ready to deploy StaffRoom? Let me know which hosting platform you'd like to use!
