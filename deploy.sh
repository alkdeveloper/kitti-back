#!/bin/bash

# Kitti Backend Deployment Script for EC2
# Usage: ./deploy.sh

set -e

echo "🚀 Starting Kitti Backend Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}Please do not run as root${NC}"
    exit 1
fi

# Project directory
PROJECT_DIR="/home/ubuntu/kitti-back"
cd $PROJECT_DIR

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Pull latest changes
echo -e "${YELLOW}Pulling latest changes from Git...${NC}"
git pull origin main

# Install/update dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
echo -e "${YELLOW}Running database migrations...${NC}"
python manage.py migrate --noinput

# Collect static files
echo -e "${YELLOW}Collecting static files...${NC}"
python manage.py collectstatic --noinput

# Create logs directory if it doesn't exist
mkdir -p logs

# Restart Gunicorn service
echo -e "${YELLOW}Restarting Gunicorn service...${NC}"
sudo systemctl restart kitti-backend

# Check service status
echo -e "${YELLOW}Checking service status...${NC}"
sleep 2
sudo systemctl status kitti-backend --no-pager

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"

