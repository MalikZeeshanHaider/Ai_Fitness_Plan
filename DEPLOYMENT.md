# Deployment Guide

Complete guide for deploying the **AI Gym Workout Recommendation System** to production.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Production Deployment](#production-deployment)
- [Cloud Deployment Options](#cloud-deployment-options)
- [Docker Deployment](#docker-deployment)
- [Environment Configuration](#environment-configuration)
- [Performance Optimization](#performance-optimization)
- [Monitoring and Logging](#monitoring-and-logging)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **Python**: 3.10 or higher
- **RAM**: Minimum 2GB (4GB recommended)
- **Storage**: 500MB free space
- **OS**: Windows, macOS, or Linux

### Required Software

```bash
# Python 3.10+
python --version

# pip (package manager)
pip --version

# Git (for version control)
git --version
```

---

## Local Development Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd AI_GYM_PROJECT
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create `.env` file from template:

```bash
cp .env.example .env
```

Edit `.env`:
```env
# Application Settings
APP_NAME=AI Gym Workout Recommender
DEBUG=True
LOG_LEVEL=INFO

# Data Settings
DATA_PATH=data/GymDataset.csv
CACHE_ENABLED=True
CACHE_TTL=3600

# Performance Settings
MAX_CACHE_SIZE=1000
BATCH_SIZE=100
```

### 5. Initialize Data

```bash
# Generate sample dataset if not present
python src/infrastructure/data/data_loader.py
```

### 6. Run Application

```bash
streamlit run src/presentation/app.py
```

Application will be available at: `http://localhost:8501`

---

## Production Deployment

### 1. Prepare Application

Update configuration for production:

**config/config.yaml:**
```yaml
app:
  name: "AI Gym Workout Recommender"
  version: "1.0.0"
  environment: production
  debug: false

performance:
  cache_enabled: true
  cache_ttl: 3600
  max_workers: 4
  timeout: 30

logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: logs/production.log
  max_bytes: 10485760  # 10MB
  backup_count: 5

security:
  enable_ssl: true
  allowed_hosts: ["yourdomain.com", "www.yourdomain.com"]
```

### 2. Install Production Dependencies

```bash
pip install gunicorn  # WSGI server
pip install supervisor  # Process manager
```

### 3. Create Start Script

**scripts/start_production.sh:**
```bash
#!/bin/bash
set -e

# Activate virtual environment
source venv/bin/activate

# Export environment variables
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Start application
streamlit run src/presentation/app.py \
  --server.port $STREAMLIT_SERVER_PORT \
  --server.address $STREAMLIT_SERVER_ADDRESS \
  --server.headless true \
  --browser.gatherUsageStats false \
  --logger.level info
```

Make executable:
```bash
chmod +x scripts/start_production.sh
```

### 4. Setup Process Manager

**supervisor/ai_gym_app.conf:**
```ini
[program:ai_gym_app]
command=/path/to/AI_GYM_PROJECT/scripts/start_production.sh
directory=/path/to/AI_GYM_PROJECT
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/ai_gym_app.err.log
stdout_logfile=/var/log/ai_gym_app.out.log
environment=PATH="/path/to/AI_GYM_PROJECT/venv/bin"
```

### 5. Configure Reverse Proxy (Nginx)

**/etc/nginx/sites-available/ai_gym_app:**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/ai_gym_app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 6. Setup SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Cloud Deployment Options

### Option 1: Streamlit Cloud (Easiest)

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <github-url>
git push -u origin main
```

2. **Deploy to Streamlit Cloud**
- Go to [share.streamlit.io](https://share.streamlit.io)
- Connect GitHub repository
- Select `src/presentation/app.py` as main file
- Click "Deploy"

**Pros:**
- Free for public repositories
- Zero configuration
- Automatic HTTPS
- Built-in monitoring

**Cons:**
- Resource limitations
- Public access required

### Option 2: AWS EC2

**Launch Instance:**
```bash
# SSH into EC2
ssh -i keypair.pem ubuntu@ec2-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.10
sudo apt install python3.10 python3.10-venv python3-pip -y

# Clone repository
git clone <repository-url>
cd AI_GYM_PROJECT

# Setup and run (follow Local Development Setup)
```

**Configure Security Group:**
- Allow inbound TCP on port 8501
- Allow inbound TCP on port 80 (HTTP)
- Allow inbound TCP on port 443 (HTTPS)

### Option 3: Heroku

**Procfile:**
```
web: streamlit run src/presentation/app.py --server.port=$PORT --server.address=0.0.0.0
```

**runtime.txt:**
```
python-3.10.0
```

**Deploy:**
```bash
heroku create ai-gym-recommender
git push heroku main
```

### Option 4: Google Cloud Run

**Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "src/presentation/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Deploy:**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-gym-app
gcloud run deploy ai-gym-app --image gcr.io/PROJECT_ID/ai-gym-app --platform managed
```

### Option 5: Azure App Service

```bash
az webapp up --name ai-gym-recommender --runtime "PYTHON:3.10"
```

---

## Docker Deployment

### Dockerfile

**Dockerfile:**
```dockerfile
# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p logs data/cache

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run application
CMD ["streamlit", "run", "src/presentation/app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
```

### Docker Compose

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  ai-gym-app:
    build: .
    container_name: ai_gym_recommender
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./config:/app/config
    environment:
      - DEBUG=False
      - LOG_LEVEL=INFO
      - CACHE_ENABLED=True
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Build and Run

```bash
# Build image
docker build -t ai-gym-recommender:latest .

# Run container
docker run -d \
  --name ai_gym_app \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  ai-gym-recommender:latest

# Or use Docker Compose
docker-compose up -d

# View logs
docker logs -f ai_gym_app

# Stop container
docker stop ai_gym_app

# Remove container
docker rm ai_gym_app
```

---

## Environment Configuration

### Environment Variables

**Production .env:**
```env
# Application
APP_ENV=production
DEBUG=False
LOG_LEVEL=INFO

# Database
DATA_PATH=data/GymDataset.csv
CACHE_PATH=data/cache

# Performance
CACHE_ENABLED=True
CACHE_TTL=3600
MAX_CACHE_SIZE=1000
BATCH_SIZE=100

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Monitoring
ENABLE_METRICS=True
METRICS_PORT=9090
```

### Streamlit Configuration

**.streamlit/config.toml:**
```toml
[server]
port = 8501
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[logger]
level = "info"
```

---

## Performance Optimization

### 1. Enable Caching

All caching is built-in. Ensure `CACHE_ENABLED=True` in `.env`.

### 2. Optimize Data Loading

Data is automatically cached. For custom optimization:

```python
from src.utils.performance_optimizer import cached, monitor_performance

@cached(cache_type="exercise")
@monitor_performance("custom_operation")
def your_function():
    # Your code
    pass
```

### 3. Resource Limits

Set in `config/config.yaml`:
```yaml
performance:
  max_workers: 4
  timeout: 30
  max_memory_mb: 2048
```

### 4. Database Optimization

For production with large datasets:
- Use PostgreSQL or MySQL instead of CSV
- Enable connection pooling
- Add database indexes

---

## Monitoring and Logging

### Application Logs

**Location:** `logs/production.log`

**View logs:**
```bash
tail -f logs/production.log
```

### Performance Metrics

Access performance report:
```python
from src.utils.performance_optimizer import PerformanceOptimizer

report = PerformanceOptimizer.get_performance_report()
print(report)
```

### Health Check Endpoint

Streamlit provides built-in health check:
```
http://your-domain.com/_stcore/health
```

### Error Tracking

Integrate Sentry (optional):

```bash
pip install sentry-sdk
```

**src/presentation/app.py:**
```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
    environment="production"
)
```

---

## Security Considerations

### 1. Input Validation

All inputs are validated by `InputValidator` class (built-in).

### 2. HTTPS

Always use HTTPS in production (configured via nginx/certbot above).

### 3. Environment Variables

Never commit `.env` file. Use `.env.example` as template.

### 4. Rate Limiting

Add to nginx config:
```nginx
limit_req_zone $binary_remote_addr zone=mylimit:10m rate=10r/s;

server {
    location / {
        limit_req zone=mylimit burst=20;
        # ... rest of config
    }
}
```

### 5. Security Headers

Add to nginx:
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
```

---

## Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Find process using port
lsof -i :8501

# Kill process
kill -9 <PID>
```

**2. Module Not Found**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**3. Data Loading Error**
```bash
# Regenerate dataset
python src/infrastructure/data/data_loader.py

# Check file exists
ls data/GymDataset.csv
```

**4. Memory Issues**
- Reduce `MAX_CACHE_SIZE` in `.env`
- Clear cache: `rm -rf data/cache/*`
- Restart application

**5. Slow Performance**
- Enable caching: `CACHE_ENABLED=True`
- Increase cache TTL: `CACHE_TTL=7200`
- Check performance report (see Monitoring section)

### Debug Mode

Enable debug logging:

**.env:**
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

View detailed logs:
```bash
tail -f logs/production.log | grep ERROR
```

### Support

For issues:
1. Check logs: `logs/production.log`
2. Review error messages
3. Check configuration files
4. Refer to [USAGE_GUIDE.md](docs/USAGE_GUIDE.md)

---

## Post-Deployment Checklist

- [ ] Application runs without errors
- [ ] All dependencies installed
- [ ] Environment variables configured
- [ ] Data files present and valid
- [ ] HTTPS enabled (production)
- [ ] Reverse proxy configured (production)
- [ ] Process manager running (production)
- [ ] Logs being written
- [ ] Health check responding
- [ ] Performance monitoring active
- [ ] Backup strategy in place
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Error tracking configured (optional)

---

## Scaling Considerations

For high-traffic scenarios:

1. **Horizontal Scaling:** Deploy multiple instances behind load balancer
2. **Database:** Migrate from CSV to PostgreSQL/MySQL
3. **Caching:** Use Redis for distributed caching
4. **CDN:** Serve static assets via CDN
5. **Container Orchestration:** Use Kubernetes for auto-scaling

---

## Backup and Recovery

**Backup data directory:**
```bash
tar -czf backup-$(date +%Y%m%d).tar.gz data/
```

**Automated backup (crontab):**
```bash
0 2 * * * cd /path/to/AI_GYM_PROJECT && tar -czf backups/backup-$(date +\%Y\%m\%d).tar.gz data/
```

**Restore:**
```bash
tar -xzf backup-20240101.tar.gz
```

---

## Maintenance

**Regular tasks:**
- Monitor logs for errors
- Check disk space
- Update dependencies monthly
- Review performance metrics
- Clear old cache files
- Backup data weekly

**Update application:**
```bash
git pull origin main
pip install -r requirements.txt --upgrade
sudo systemctl restart ai_gym_app  # If using supervisor
```

---

## Conclusion

Your **AI Gym Workout Recommendation System** is now ready for production deployment!

For additional help:
- **Documentation:** [README.md](README.md)
- **Architecture:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Algorithms:** [docs/ALGORITHMS.md](docs/ALGORITHMS.md)
- **Usage Guide:** [docs/USAGE_GUIDE.md](docs/USAGE_GUIDE.md)

**Good luck with your deployment! 🚀💪**
