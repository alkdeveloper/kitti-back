# 🚀 BOSOFT Kitti Platform

**Professional Product Management System**

[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![API](https://img.shields.io/badge/API-REST-orange.svg)](https://www.django-rest-framework.org/)
[![BOSOFT](https://img.shields.io/badge/Made%20by-BOSOFT-red.svg)](https://bosoft.com)

Modern, scalable product management system with multilingual support, REST API, and professional admin interface.

## ✨ Features

- 🌍 **Multilingual Support** - Turkish & English content management
- 🔧 **REST API** - Complete API with Swagger documentation
- 🎨 **Modern Admin** - Beautiful Jazzmin admin interface
- 📱 **Responsive Design** - Mobile-friendly interface
- 🌳 **Hierarchical Data** - MPTT-based category/product structure
- 🖼️ **Image Management** - Multi-language image support
- 📊 **API Documentation** - Auto-generated Swagger/OpenAPI docs

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd kitti
```

### 2. Setup Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings (optional)
# Default values work out of the box!
```

### 4. Launch Platform 🚀
```bash
python manage.py run
```

**That's it!** 🎉

The BOSOFT Kitti Platform will automatically:
- ✅ Initialize database
- ✅ Create admin user
- ✅ Collect static files
- ✅ Start development server
- ✅ Open your browser (with `--open-browser`)

## 🎯 Access Points

After running `python manage.py run`, visit:

- **🔗 Admin Panel**: http://127.0.0.1:8000/admin/
- **📚 API Documentation**: http://127.0.0.1:8000/api/docs/
- **🔍 API Schema**: http://127.0.0.1:8000/api/schema/
- **📋 Categories API**: http://127.0.0.1:8000/api/categories/
- **📦 Products API**: http://127.0.0.1:8000/api/products/
- **🖼️ Sliders API**: http://127.0.0.1:8000/api/sliders/

## 👤 Default Credentials
```bash
Username: admin
Password: admin123
```

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Django Settings
SECRET_KEY=super-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Admin User
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin123
DJANGO_SUPERUSER_EMAIL=admin@example.com
```

### Sample Data

Generate sample categories, products, and sliders:

```bash
python manage.py run --fake-data
```

Add sample images to these directories:
- `static/fake_data/product_images/` - Product images
- `static/fake_data/sliders/` - Banner images

## 🛠️ Advanced Usage

### Command Options

```bash
# Basic launch
python manage.py run

# With sample data
python manage.py run --fake-data

# Open browser automatically
python manage.py run --open-browser

# Custom port
python manage.py run --port 8080

# Setup without starting server
python manage.py run --no-server

# Clear existing sample data
python manage.py run --fake-data --clear-data

# Skip static collection (faster)
python manage.py run --skip-static

# Development mode (skip migrations)
python manage.py run --skip-migrate --skip-static
```

### Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Database setup
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py create_default_superuser

# Collect static files
python manage.py collectstatic --noinput

# Start server
python manage.py runserver
```

## 📁 Project Structure
```bash
kitti/
├── 📁 products/ # Main app
│ ├── 📁 models/ # Item, Slider models
│ ├── 📁 serializers/ # API serializers
│ ├── 📁 views/ # API views
│ └── 📁 admin/ # Admin configuration
├── 📁 static/ # Static files
│ └── 📁 fake_data/ # Sample images
├── 📁 media/ # Uploaded files
├── 📄 .env.example # Environment template
├── 📄 requirements.txt # Dependencies
└── 📄 manage.py # Django management
```

## 🌍 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/` | GET | API information |
| `/api/categories/` | GET | List categories with products |
| `/api/products/` | GET | List all products |
| `/api/sliders/` | GET | List slider banners |
| `/api/docs/` | GET | Swagger documentation |
| `/api/schema/` | GET | OpenAPI schema |

### API Features

- 🔍 **Search & Filter** - Search products by name, filter by category
- 🌐 **Multi-language** - Use `?lang=tr` or `?lang=en` parameter
- 📄 **Pagination** - Automatic pagination for large datasets
- 📝 **Documentation** - Complete Swagger/OpenAPI documentation

### Example API Calls

```bash
# Get all categories with products (Turkish)
curl http://127.0.0.1:8000/api/categories/?lang=tr

# Get all products (English)
curl http://127.0.0.1:8000/api/products/?lang=en

# Search products
curl http://127.0.0.1:8000/api/products/?search=laptop

# Filter by category
curl http://127.0.0.1:8000/api/products/?category=1
```

## 🔧 Development

### Requirements

- Python 3.8+
- Django 5.0+
- See `requirements.txt` for full dependencies

### Key Packages

- **Django REST Framework** - API development
- **django-modeltranslation** - Multi-language support
- **django-mptt** - Hierarchical data
- **django-jazzmin** - Modern admin interface
- **drf-spectacular** - API documentation
- **Faker** - Sample data generation

## 📚 Documentation

- **API Docs**: Available at `/api/docs/` when server is running
- **Admin Guide**: Login to `/admin/` for content management
- **Multi-language**: Switch between Turkish/English in admin and API

## 🎨 Screenshots

### Admin Panel
Professional Jazzmin interface with hierarchical product management.

### API Documentation
Complete Swagger documentation with interactive API explorer.

### Multi-language Support
Seamless Turkish/English content management.

## 🆘 Support

### Common Issues

**Port already in use?**
```bash
python manage.py run --port 8080
```

**Database issues?**
```bash
rm db.sqlite3
python manage.py run
```

**Static files not loading?**
```bash
python manage.py run --skip-static
# Or manually: python manage.py collectstatic
```

### Need Help?

- 📧 Contact: BOSOFT Support
- 📖 Documentation: `/api/docs/`
- 🐛 Issues: Create issue in repository

## 📄 License

**BOSOFT Kitti Platform** - Professional Product Management System

---

<div align="center">

**💼 Made with ❤️ by BOSOFT**

*Excellence in Software Development*

[![BOSOFT](https://img.shields.io/badge/BOSOFT-Professional%20Software%20Solutions-red.svg?style=for-the-badge)](https://bosoft.com)

</div>