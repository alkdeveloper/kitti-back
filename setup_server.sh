#!/bin/bash

# EC2 Server Initial Setup Script
# Bu script'i EC2'ye ilk bağlandığınızda çalıştırın
# Usage: ./setup_server.sh

set -e

echo "🔧 Starting EC2 Server Setup..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Update system
echo -e "${YELLOW}Updating system packages...${NC}"
sudo apt update && sudo apt upgrade -y

# Install essential packages
echo -e "${YELLOW}Installing essential packages...${NC}"
sudo apt install -y \
    build-essential \
    curl \
    git \
    nginx \
    python3-pip \
    python3-venv \
    certbot \
    python3-certbot-nginx \
    ufw \
    htop \
    unzip

# Install Node.js 18.x
echo -e "${YELLOW}Installing Node.js 18.x...${NC}"
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2
echo -e "${YELLOW}Installing PM2...${NC}"
sudo npm install -g pm2

# Setup PM2 startup
echo -e "${YELLOW}Setting up PM2 startup...${NC}"
pm2 startup systemd | grep "sudo" | bash || true

# Configure firewall
echo -e "${YELLOW}Configuring firewall...${NC}"
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# Create project directories
echo -e "${YELLOW}Creating project directories...${NC}"
mkdir -p /home/ubuntu/kitti-back
mkdir -p /home/ubuntu/kitti

echo -e "${GREEN}✅ Server setup completed!${NC}"
echo ""
echo "Next steps:"
echo "1. Clone backend: cd /home/ubuntu && git clone https://github.com/alkdeveloper/kitti-back.git"
echo "2. Clone frontend: cd /home/ubuntu && git clone https://github.com/alkdeveloper/kitti.git"
echo "3. Follow the deployment guide: EC2_DEPLOYMENT_GUIDE.md"

