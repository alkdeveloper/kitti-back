# 🚀 EC2 Deployment Guide - Kitti Project

Bu rehber, Kitti projesinin (Backend + Frontend) AWS EC2 üzerinde production'a alınması için adım adım talimatları içerir.

---

## 📋 İçindekiler

1. [EC2 Instance Hazırlığı](#1-ec2-instance-hazırlığı)
2. [Backend Kurulumu](#2-backend-kurulumu)
3. [Frontend Kurulumu](#3-frontend-kurulumu)
4. [Nginx Yapılandırması](#4-nginx-yapılandırması)
5. [SSL Sertifikası (Let's Encrypt)](#5-ssl-sertifikası-lets-encrypt)
6. [Firewall Yapılandırması](#6-firewall-yapılandırması)
7. [Monitoring ve Logs](#7-monitoring-ve-logs)

---

## 1. EC2 Instance Hazırlığı

### 1.1 EC2 Instance Oluşturma

1. AWS Console'da EC2 > Launch Instance
2. **AMI**: Ubuntu Server 22.04 LTS (veya daha yeni)
3. **Instance Type**: t3.medium veya daha güçlü (önerilen: t3.large)
4. **Key Pair**: Yeni bir key pair oluşturun veya mevcut olanı kullanın
5. **Security Group**: 
   - SSH (22) - Your IP
   - HTTP (80) - 0.0.0.0/0
   - HTTPS (443) - 0.0.0.0/0
   - Custom TCP (8000) - 127.0.0.1/32 (Backend için)
   - Custom TCP (3000) - 127.0.0.1/32 (Frontend için)

### 1.2 İlk Bağlantı

```bash
# SSH ile bağlan
ssh -i your-key.pem ubuntu@your-ec2-ip

# Sistem güncellemesi
sudo apt update && sudo apt upgrade -y

# Temel paketler
sudo apt install -y build-essential curl git nginx python3-pip python3-venv nodejs npm
```

### 1.3 Node.js ve PM2 Kurulumu

```bash
# Node.js 18.x kurulumu (LTS)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# PM2 kurulumu (Process Manager)
sudo npm install -g pm2

# PM2'yi startup'a ekle
pm2 startup systemd
# Çıkan komutu çalıştırın (sudo ile başlayan)
```

---

## 2. Backend Kurulumu

### 2.1 Repository'yi Klonlama

```bash
cd /home/ubuntu
git clone https://github.com/alkdeveloper/kitti-back.git
cd kitti-back
```

### 2.2 Virtual Environment ve Bağımlılıklar

```bash
# Virtual environment oluştur
python3 -m venv venv
source venv/bin/activate

# Bağımlılıkları yükle
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.3 Environment Variables

```bash
# .env dosyası oluştur
nano .env
```

`.env` dosyasına şunları ekleyin:

```bash
# Django Settings
SECRET_KEY=your-super-secret-key-here-generate-new-one
DEBUG=False
ALLOWED_HOSTS=api.yourdomain.com,your-ec2-ip,127.0.0.1,localhost

# Database (SQLite için)
DATABASE_URL=sqlite:///db.sqlite3

# PostgreSQL için (önerilen production'da):
# DATABASE_URL=postgres://user:password@localhost:5432/kitti_db

# Admin User
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=your-secure-password
DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com

# Fernet Key (yeni oluşturun)
FERNET_KEY=your-fernet-key-here

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
RECIEPENT_EMAIL=recipient@yourdomain.com

# Security
SECURE_SSL_REDIRECT=True
```

**Önemli:** `SECRET_KEY` ve `FERNET_KEY` için yeni değerler oluşturun:

```bash
# SECRET_KEY için
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# FERNET_KEY için
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 2.4 Database ve Static Files

```bash
# Migration'ları çalıştır
python manage.py migrate

# Admin kullanıcısı oluştur (eğer yoksa)
python manage.py createsuperuser

# Static dosyaları topla
python manage.py collectstatic --noinput

# Logs dizini oluştur
mkdir -p logs
```

### 2.5 Gunicorn Service Kurulumu

```bash
# Systemd service dosyasını kopyala
sudo cp kitti-backend.service /etc/systemd/system/

# Service dosyasını düzenle (gerekirse)
sudo nano /etc/systemd/system/kitti-backend.service

# Service'i başlat
sudo systemctl daemon-reload
sudo systemctl enable kitti-backend
sudo systemctl start kitti-backend

# Durumu kontrol et
sudo systemctl status kitti-backend
```

### 2.6 Test

```bash
# Backend'in çalıştığını kontrol et
curl http://127.0.0.1:8000/api/
```

---

## 3. Frontend Kurulumu

### 3.1 Repository'yi Klonlama

```bash
cd /home/ubuntu
git clone https://github.com/alkdeveloper/kitti.git
cd kitti
```

### 3.2 Bağımlılıklar ve Build

```bash
# Bağımlılıkları yükle
npm install

# Environment dosyası oluştur
nano .env.local
```

`.env.local` dosyasına:

```bash
NEXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com/api
```

```bash
# Production build
npm run build

# Logs dizini oluştur
mkdir -p logs
```

### 3.3 PM2 ile Başlatma

```bash
# PM2 config dosyasını düzenle (domain'i güncelle)
nano ecosystem.config.js

# PM2 ile başlat
pm2 start ecosystem.config.js

# PM2'yi kaydet
pm2 save
```

---

## 4. Nginx Yapılandırması

### 4.1 Backend Nginx Config

```bash
# Nginx config dosyasını kopyala
sudo cp /home/ubuntu/kitti-back/nginx.conf /etc/nginx/sites-available/kitti-backend

# Domain'i düzenle
sudo nano /etc/nginx/sites-available/kitti-backend

# Symlink oluştur
sudo ln -s /etc/nginx/sites-available/kitti-backend /etc/nginx/sites-enabled/

# Test ve restart
sudo nginx -t
sudo systemctl restart nginx
```

### 4.2 Frontend Nginx Config

```bash
# Nginx config dosyasını kopyala
sudo cp /home/ubuntu/kitti/nginx-frontend.conf /etc/nginx/sites-available/kitti-frontend

# Domain'i düzenle
sudo nano /etc/nginx/sites-available/kitti-frontend

# Symlink oluştur
sudo ln -s /etc/nginx/sites-available/kitti-frontend /etc/nginx/sites-enabled/

# Test ve restart
sudo nginx -t
sudo systemctl restart nginx
```

### 4.3 Nginx Permissions

```bash
# Static ve media dosyaları için izinler
sudo chown -R www-data:www-data /home/ubuntu/kitti-back/static
sudo chown -R www-data:www-data /home/ubuntu/kitti-back/media
sudo chown -R www-data:www-data /home/ubuntu/kitti/.next
```

---

## 5. SSL Sertifikası (Let's Encrypt)

### 5.1 Certbot Kurulumu

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 5.2 SSL Sertifikası Oluşturma

```bash
# Backend için
sudo certbot --nginx -d api.yourdomain.com

# Frontend için
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 5.3 Otomatik Yenileme

Certbot otomatik olarak cron job oluşturur. Test etmek için:

```bash
sudo certbot renew --dry-run
```

### 5.4 Nginx HTTPS Config'i Aktif Et

SSL sertifikası oluşturulduktan sonra, nginx config dosyalarındaki HTTPS bölümlerinin yorumlarını kaldırın.

---

## 6. Firewall Yapılandırması

```bash
# UFW firewall kurulumu
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Durumu kontrol et
sudo ufw status
```

---

## 7. Monitoring ve Logs

### 7.1 Backend Logs

```bash
# Gunicorn logs
tail -f /home/ubuntu/kitti-back/logs/gunicorn_error.log
tail -f /home/ubuntu/kitti-back/logs/gunicorn_access.log

# Django logs
tail -f /home/ubuntu/kitti-back/logs/django.log

# Systemd logs
sudo journalctl -u kitti-backend -f
```

### 7.2 Frontend Logs

```bash
# PM2 logs
pm2 logs kitti-frontend

# PM2 monitoring
pm2 monit
```

### 7.3 System Monitoring

```bash
# Disk usage
df -h

# Memory usage
free -h

# Process monitoring
htop
```

---

## 🔄 Deployment İşlemi

### Backend Deployment

```bash
cd /home/ubuntu/kitti-back
chmod +x deploy.sh
./deploy.sh
```

### Frontend Deployment

```bash
cd /home/ubuntu/kitti
chmod +x deploy.sh
./deploy.sh
```

---

## 🆘 Sorun Giderme

### Backend çalışmıyor

```bash
# Service durumunu kontrol et
sudo systemctl status kitti-backend

# Logs'u kontrol et
sudo journalctl -u kitti-backend -n 50

# Manuel test
cd /home/ubuntu/kitti-back
source venv/bin/activate
gunicorn kitti.wsgi:application --bind 0.0.0.0:8000
```

### Frontend çalışmıyor

```bash
# PM2 durumunu kontrol et
pm2 status
pm2 logs kitti-frontend

# Manuel test
cd /home/ubuntu/kitti
npm start
```

### Nginx hataları

```bash
# Config test
sudo nginx -t

# Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### Port kullanımda

```bash
# Port'u kullanan process'i bul
sudo lsof -i :8000
sudo lsof -i :3000

# Process'i durdur
sudo kill -9 <PID>
```

---

## 📝 Önemli Notlar

1. **SECRET_KEY**: Production'da mutlaka güçlü bir key kullanın
2. **DEBUG**: Production'da `False` olmalı
3. **ALLOWED_HOSTS**: Domain'lerinizi ekleyin
4. **Database**: Production'da PostgreSQL kullanın (SQLite önerilmez)
5. **Backup**: Düzenli backup alın
6. **Monitoring**: Uptime monitoring kullanın (UptimeRobot, Pingdom, vb.)
7. **SSL**: Mutlaka HTTPS kullanın

---

## 🔐 Güvenlik Checklist

- [ ] SECRET_KEY değiştirildi
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS yapılandırıldı
- [ ] SSL sertifikası kuruldu
- [ ] Firewall aktif
- [ ] Admin şifresi güçlü
- [ ] Database backup planı var
- [ ] Log rotation yapılandırıldı

---

**Son Güncelleme**: 2025

