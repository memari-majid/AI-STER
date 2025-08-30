# AI-STER Deployment Guide
Complete guide for deploying the AI-STER application

## Overview
This guide covers all deployment options for AI-STER, from local development to cloud production environments.

## Table of Contents
1. [Local Development](#local-development)
2. [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
3. [Production Deployment](#production-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Secrets Management](#secrets-management)
6. [Troubleshooting](#troubleshooting)

## Local Development

### Prerequisites
- Python 3.8+
- Git
- Virtual environment tool (venv/conda)

### Setup Steps

1. **Clone Repository**
```bash
git clone https://github.com/your-org/ai-ster.git
cd ai-ster
```

2. **Create Virtual Environment**
```bash
python -m venv ai-ster-env
source ai-ster-env/bin/activate  # On Windows: ai-ster-env\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
# Copy template
cp env.example .env

# Edit .env with your values
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5-mini
```

5. **Run Application**
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Streamlit Cloud Deployment

### Prerequisites
- GitHub account
- Streamlit Cloud account (free tier available)
- Repository must be public or you need Streamlit Cloud Pro

### Deployment Steps

1. **Prepare Repository**
   - Ensure `requirements.txt` is up to date
   - Remove any sensitive data from code
   - Commit and push to GitHub

2. **Connect to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub account

3. **Configure App**
   - Repository: `your-username/ai-ster`
   - Branch: `main`
   - Main file path: `app.py`

4. **Set Up Secrets**
   - Click "Advanced settings"
   - Navigate to "Secrets"
   - Add your secrets in TOML format:

```toml
# Streamlit Cloud Secrets Format
OPENAI_API_KEY = "sk-..."
OPENAI_MODEL = "gpt-5-mini"

# Optional: Database credentials
[database]
host = "your-host"
port = 5432
database = "ai_ster_db"
username = "db_user"
password = "db_password"
```

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (5-10 minutes)
   - Your app will be available at: `https://your-app-name.streamlit.app`

### Streamlit Cloud Features

#### Auto-deployment
- Automatic deployment on git push
- Branch-based deployments
- Rollback capabilities

#### Resource Limits (Free Tier)
- 1 GB RAM
- 1 GB storage
- Community cloud resources

#### Custom Domain (Pro)
- Configure custom domain in app settings
- SSL certificates handled automatically

## Production Deployment

### Option 1: AWS EC2

1. **Launch EC2 Instance**
   - Ubuntu 20.04 LTS
   - t3.medium or larger
   - Security group: Allow ports 22, 80, 443, 8501

2. **Server Setup**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# Clone repository
git clone https://github.com/your-org/ai-ster.git
cd ai-ster

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

3. **Configure Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

4. **Create Systemd Service**
```ini
[Unit]
Description=AI-STER Streamlit App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ai-ster
Environment="PATH=/home/ubuntu/ai-ster/venv/bin"
Environment="OPENAI_MODEL=gpt-5-mini"
ExecStart=/home/ubuntu/ai-ster/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

5. **Enable and Start Service**
```bash
sudo systemctl enable ai-ster
sudo systemctl start ai-ster
```

### Option 2: Docker Deployment

1. **Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **Build and Run**
```bash
docker build -t ai-ster .
docker run -p 8501:8501 --env-file .env ai-ster
```

### Option 3: Kubernetes Deployment

See `kubernetes/` directory for manifests and helm charts.

## Environment Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | `sk-...` |
| `APP_PASSWORD` | Password for app access | `secure-password-123` |
| `ADMIN_PASSWORD` | Admin panel password | `admin-secure-456` |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `STREAMLIT_THEME` | UI theme | `light` |
| `MAX_FILE_SIZE` | Max upload size (MB) | `200` |
| `SESSION_TIMEOUT` | Session timeout (minutes) | `120` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Database Configuration (Future)

```env
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://localhost:6379
```

## Secrets Management

### Best Practices

1. **Never commit secrets to git**
   - Use `.gitignore` for `.env` files
   - Use environment variables
   - Use secret management services

2. **Rotate secrets regularly**
   - API keys every 90 days
   - Passwords every 60 days
   - Document rotation schedule

3. **Use different secrets per environment**
   - Development secrets
   - Staging secrets
   - Production secrets

### Secret Storage Options

#### 1. Environment Variables
```bash
export OPENAI_API_KEY="sk-..."
```

#### 2. `.env` File (Local Only)
```env
OPENAI_API_KEY=sk-...
APP_PASSWORD=password123
```

#### 3. AWS Secrets Manager
```python
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']
```

#### 4. HashiCorp Vault
```python
import hvac

client = hvac.Client(url='https://vault.example.com')
secret = client.read('secret/data/ai-ster')
```

## Monitoring and Maintenance

### Health Checks

1. **Application Health**
```python
# Add to app.py
@st.cache_data
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }
```

2. **Monitoring Setup**
- Use Datadog, New Relic, or CloudWatch
- Monitor response times
- Track error rates
- Set up alerts

### Backup Strategy

1. **Data Backup**
```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf backup_$DATE.tar.gz data_storage/
aws s3 cp backup_$DATE.tar.gz s3://your-backup-bucket/
```

2. **Database Backup**
```bash
pg_dump -U username -d ai_ster > backup_$DATE.sql
```

### Update Process

1. **Test in staging**
2. **Backup production data**
3. **Deploy during low-usage hours**
4. **Monitor for issues**
5. **Have rollback plan ready**

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port 8501
lsof -i :8501
# Kill the process
kill -9 <PID>
```

#### Module Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

#### Streamlit Cloud Build Failures
- Check `requirements.txt` for typos
- Ensure all dependencies are pip-installable
- Check Python version compatibility
- Review build logs in Streamlit Cloud

#### Memory Issues
- Increase server resources
- Implement caching strategies
- Optimize data loading
- Use connection pooling

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Optimization

1. **Enable Caching**
```python
@st.cache_data
def load_data():
    return pd.read_csv('data.csv')
```

2. **Optimize Session State**
- Clear unused state variables
- Implement state cleanup on logout

3. **Database Connection Pooling**
```python
from sqlalchemy.pool import QueuePool
engine = create_engine(url, poolclass=QueuePool)
```

## Security Considerations

### HTTPS Setup

1. **Let's Encrypt SSL**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

2. **Auto-renewal**
```bash
sudo certbot renew --dry-run
```

### Security Headers

Add to Nginx config:
```nginx
add_header X-Frame-Options "SAMEORIGIN";
add_header X-Content-Type-Options "nosniff";
add_header X-XSS-Protection "1; mode=block";
```

### Access Control

1. **IP Whitelisting**
```nginx
location /admin {
    allow 192.168.1.0/24;
    deny all;
}
```

2. **Rate Limiting**
```nginx
limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;
```

## Support and Resources

- **Documentation**: [GitHub Wiki](https://github.com/your-org/ai-ster/wiki)
- **Issues**: [GitHub Issues](https://github.com/your-org/ai-ster/issues)
- **Community**: [Discord Server](https://discord.gg/ai-ster)
- **Email**: support@ai-ster.edu

---

*Last Updated: December 2024*
*Version: 2.0*
*For AI-STER v1.0.0* 