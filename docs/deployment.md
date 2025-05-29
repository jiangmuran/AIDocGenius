# AIDocGenius 部署指南

## 环境要求

- Python 3.8+
- 4GB+ RAM
- 10GB+ 磁盘空间
- NVIDIA GPU (可选，用于加速)

## 部署选项

### 1. Docker部署（推荐）

最简单的部署方式是使用Docker和Docker Compose。

1. 安装Docker和Docker Compose：
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# CentOS
sudo yum install docker docker-compose
```

2. 克隆项目：
```bash
git clone https://github.com/jiangmuran/AIDocGenius.git
cd AIDocGenius
```

3. 构建和启动服务：
```bash
docker-compose up -d
```

4. 检查服务状态：
```bash
docker-compose ps
docker-compose logs -f
```

### 2. 直接部署

如果您不想使用Docker，可以直接在服务器上部署。

1. 安装Python和依赖：
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.8 python3.8-venv python3-pip

# CentOS
sudo yum install python38 python38-devel
```

2. 创建虚拟环境：
```bash
python3.8 -m venv venv
source venv/bin/activate
```

3. 安装项目：
```bash
pip install -e .
```

4. 使用Gunicorn启动服务：
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker aidocgenius.api:app
```

### 3. 使用Nginx代理

建议使用Nginx作为反向代理：

1. 安装Nginx：
```bash
# Ubuntu/Debian
sudo apt-get install nginx

# CentOS
sudo yum install nginx
```

2. 配置Nginx：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/your/static/files;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
}
```

3. 启动Nginx：
```bash
sudo systemctl restart nginx
```

## 环境配置

### 1. 环境变量

可以通过环境变量配置以下选项：

```bash
# 基本配置
export DEBUG=0
export HOST=0.0.0.0
export PORT=8000

# 安全配置
export SECRET_KEY=your-secret-key
export ALLOWED_HOSTS=your-domain.com

# 性能配置
export WORKERS=4
export TIMEOUT=120
```

### 2. SSL证书

建议使用Let's Encrypt获取免费SSL证书：

```bash
# 安装certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com
```

## 监控和维护

### 1. 日志管理

配置日志轮转：

```bash
# /etc/logrotate.d/aidocgenius
/var/log/aidocgenius/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload aidocgenius
    endscript
}
```

### 2. 备份

设置定期备份：

```bash
#!/bin/bash
# /usr/local/bin/backup-aidocgenius.sh

BACKUP_DIR="/var/backups/aidocgenius"
DATE=$(date +%Y%m%d)

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份数据
tar -czf "$BACKUP_DIR/aidocgenius-$DATE.tar.gz" /path/to/data

# 保留最近30天的备份
find "$BACKUP_DIR" -type f -mtime +30 -delete
```

### 3. 监控

使用Prometheus和Grafana进行监控：

1. 安装Prometheus：
```bash
wget https://github.com/prometheus/prometheus/releases/download/v2.30.3/prometheus-2.30.3.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
cd prometheus-*
```

2. 配置监控：
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'aidocgenius'
    static_configs:
      - targets: ['localhost:8000']
```

## 故障排除

### 1. 常见问题

1. 服务无法启动
```bash
# 检查日志
journalctl -u aidocgenius
# 检查端口
netstat -tulpn | grep 8000
```

2. 性能问题
```bash
# 检查CPU使用
top -u aidocgenius
# 检查内存
free -m
```

### 2. 性能优化

1. 使用缓存：
```python
# 配置Redis缓存
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

2. 优化静态文件：
```nginx
# Nginx配置
location /static {
    expires max;
    add_header Cache-Control "public, no-transform";
}
```

## 安全建议

1. 启用防火墙：
```bash
# Ubuntu/Debian
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# CentOS
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

2. 设置安全headers：
```nginx
# Nginx安全配置
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

## 更新流程

1. 备份当前版本：
```bash
cp -r /path/to/aidocgenius /path/to/aidocgenius.bak
```

2. 更新代码：
```bash
git pull origin main
```

3. 更新依赖：
```bash
pip install -e .
```

4. 重启服务：
```bash
sudo systemctl restart aidocgenius
``` 