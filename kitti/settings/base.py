import os
import environ
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Environ setup
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="insecure-secret")

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

DJANGO_SUPERUSER_USERNAME = env("DJANGO_SUPERUSER_USERNAME", default="admin")
DJANGO_SUPERUSER_PASSWORD = env("DJANGO_SUPERUSER_PASSWORD", default="admin123")
DJANGO_SUPERUSER_EMAIL = env("DJANGO_SUPERUSER_EMAIL", default="admin@example.com")

# Application definition
INSTALLED_APPS = [
    "corsheaders",
    "jazzmin",
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "drf_spectacular",
    "adminsortable2",
    "mptt",
    "ckeditor",
    
    # Django App
    "products",
    "site_settings",
]

LANGUAGES = [
    ('tr', 'Türkçe'),
    ('en', 'English'),
]

LANGUAGE_CODE = 'tr'  # Varsayılan dil

# Modeltranslation ayarları
MODELTRANSLATION_DEFAULT_LANGUAGE = 'tr'
MODELTRANSLATION_LANGUAGES = ('tr', 'en')

# Opsiyonel: Fallback ayarları
MODELTRANSLATION_FALLBACK_LANGUAGES = {
    'default': ('tr', 'en'),
    'tr': ('en',),
    'en': ('tr',),
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "kitti.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "kitti.wsgi.application"

# Database (şimdilik sqlite, sonra Postgres’e geçeriz)
DATABASES = {
    "default": env.db(default=f"sqlite:///{BASE_DIR}/db.sqlite3")
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "tr"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_TZ = True

# Static files
# URL to serve static files (CSS, JavaScript, images)
STATIC_URL = "/static/"

# Directories where Django will look for additional static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]

# collectstatic'ın biriktireceği HEDEF klasör (mutlaka dosya sistemi yolu!)
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Swagger and Redoc conf:
# REST Framework ayarları
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Kitti API',
    'DESCRIPTION': 'Kitti ürün ve kategori yönetim API sistemi',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': '/api/',
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
}


# Jazzmin Konfigürasyonu
JAZZMIN_SETTINGS = {
    # Title
    "site_title": "Kitti Admin",
    "site_header": "Kitti",
    "site_brand": "Kitti Management",
    "site_logo": "admin/images/kitti-logo.svg",
    "login_logo": "admin/images/kitti-logo.svg",
    "login_logo_dark": None,
    "site_logo_classes": "img-fluid",
    "site_icon": "admin/images/kitti-logo.svg",
    
    # Welcome text
    "welcome_sign": "Kitti Admin Paneline Hoş Geldiniz",
    "copyright": "Kitti",
    
    # Search model
    "search_model": ["products.Item"],
    
    # User model avatar
    "user_avatar": None,
    
    ############
    # Top Menu #
    ############
    "topmenu_links": [
        {"name": "Ana Sayfa", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Site", "url": "/", "new_window": True},
        {"model": "auth.User"},
        {"app": "products"},
    ],
    
    #############
    # User Menu #
    #############
    "usermenu_links": [
        {"name": "Site", "url": "/", "new_window": True},
        {"model": "auth.user"}
    ],
    
    #############
    # Side Menu #
    #############
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": ["auth.Group"],
    
    # GÜNCELLENDİ: Uygulama ve model sıralaması
    "order_with_respect_to": [
        "site_settings", # Sözlük yerine sadece app adı yazıldı
        "products",
        "auth",
    ],
    
    # GÜNCELLENDİ: Yeni ikonlar eklendi
    "icons": {
        # Mevcut ikonlar
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "products": "fas fa-shopping-cart",
        "products.Item": "fas fa-boxes",
        "products.ItemImage": "fas fa-images",

        # Site Yönetimi için yeni ikonlar
        "site_settings": "fas fa-cogs",
        "site_settings.SiteSettings": "fas fa-tools",
        "site_settings.MenuItem": "fas fa-bars",
        "site_settings.Header": "fas fa-desktop",
        "site_settings.GenericSection": "fas fa-puzzle-piece",
        "site_settings.GenericSectionOurStory": "fas fa-book-open",
        "site_settings.GenericSectionContact": "fas fa-map-marker-alt",
        "site_settings.GenericSectionWholesale": "fas fa-truck-loading",
        "site_settings.FooterInfo": "fas fa-info-circle",
        "site_settings.FooterPolicy": "fas fa-file-contract",
        "site_settings.SocialMedia": "fas fa-share-alt",
    },
    
    # Default icons
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    # Related Modal
    "related_modal_active": False,
    
    #############
    # UI Tweaks #
    #############
    "custom_css": "admin/css/custom_jazzmin.css",
    "custom_js": "admin/js/custom_jazzmin.js",
    "use_google_fonts_cdn": True,
    "show_ui_builder": True,
    
    # Change view
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible", 
        "auth.group": "vertical_tabs"
    },
}

# JAZZMIN_UI_TWEAKS = {
#     "navbar_small_text": False,
#     "footer_small_text": False,
#     "body_small_text": False,
#     "brand_small_text": False,
#     "brand_colour": False,
#     "accent": "accent-primary",
#     "navbar": "navbar-dark",
#     "no_navbar_border": False,
#     "navbar_fixed": True,
#     "layout_boxed": False,
#     "footer_fixed": True,
#     "sidebar_fixed": False,
#     "sidebar": "sidebar-dark-primary",
#     "sidebar_nav_small_text": False,
#     "sidebar_disable_expand": False,
#     "sidebar_nav_child_indent": False,
#     "sidebar_nav_compact_style": False,
#     "sidebar_nav_legacy_style": True,
#     "sidebar_nav_flat_style": True,
#     "theme": "cyborg",
#     "dark_mode_theme": "None",
#     "button_classes": {
#         "primary": "btn-primary",
#         "secondary": "btn-secondary",
#         "info": "btn-info",
#         "warning": "btn-warning",
#         "danger": "btn-danger",
#         "success": "btn-success"
#     },
#     "actions_sticky_top": False
# }

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True