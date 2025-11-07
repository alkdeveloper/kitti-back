# 🚀 BOSOFT Kitti Platform

**Professional Product Management System**

[![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![API](https://img.shields.io/badge/API-REST-orange.svg)](https://www.django-rest-framework.org/)
[![BOSOFT](https://img.shields.io/badge/Made%20by-BOSOFT-red.svg)](https://bionluk.com/bologo)

Modern, scalable product management system with multilingual support, REST API, and professional admin interface.

---

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Gereksinimler](#-gereksinimler)
- [Kurulum](#-kurulum)
- [Yapılandırma](#-yapılandırma)
- [Kullanım](#-kullanım)
- [API Dokümantasyonu](#-api-dokümantasyonu)
- [Proje Yapısı](#-proje-yapısı)
- [Sorun Giderme](#-sorun-giderme)

---

## ✨ Özellikler

- 🌍 **Çok Dilli Destek** - Türkçe & İngilizce içerik yönetimi
- 🔧 **REST API** - Swagger dokümantasyonlu tam API
- 🎨 **Modern Admin** - Jazzmin admin arayüzü
- 📱 **Responsive Tasarım** - Mobil uyumlu arayüz
- 🌳 **Hiyerarşik Veri** - MPTT tabanlı kategori/ürün yapısı
- 🖼️ **Görsel Yönetimi** - Çok dilli görsel desteği
- 📊 **API Dokümantasyonu** - Otomatik Swagger/OpenAPI dokümantasyonu
- 🔐 **Güvenlik** - Şifreleme ve güvenli email gönderimi

---

## 🔧 Gereksinimler

### Sistem Gereksinimleri

- **Python**: 3.8 veya üzeri
- **Django**: 5.2.6
- **Veritabanı**: SQLite (varsayılan) veya PostgreSQL
- **İşletim Sistemi**: Windows, macOS, Linux

### Python Paketleri

Tüm gerekli paketler `requirements.txt` dosyasında listelenmiştir:

```
Django==5.2.6
djangorestframework==3.16.1
django-modeltranslation==0.19.17
django-mptt==0.18.0
django-jazzmin==3.0.1
drf-spectacular==0.28.0
django-cors-headers==4.9.0
django-environ==0.12.0
django-filter==25.1
django-cryptography==1.1
Pillow==11.3.0
Faker==37.8.0
```

---

## 🚀 Kurulum

### 1. Repository'yi Klonlayın

```bash
git clone <repository-url>
cd kitti-backend
```

### 2. Virtual Environment Oluşturun

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Environment Dosyasını Yapılandırın

Proje zaten `.env` dosyası içeriyor. Eğer yoksa `.env-example` dosyasını kopyalayın:

```bash
# .env dosyası zaten mevcut, gerekirse düzenleyin
# veya yeni bir .env oluşturmak için:
cp .env-example .env
```

### 5. Projeyi Başlatın

**Otomatik Kurulum (Önerilen):**
```bash
python manage.py run
```

Bu komut otomatik olarak:
- ✅ Veritabanı migration'larını çalıştırır
- ✅ Admin kullanıcısı oluşturur
- ✅ Static dosyaları toplar
- ✅ Development server'ı başlatır

**Manuel Kurulum:**
```bash
# Migration'ları çalıştır
python manage.py makemigrations
python manage.py migrate

# Admin kullanıcısı oluştur
python manage.py create_default_superuser

# Static dosyaları topla
python manage.py collectstatic --noinput

# Server'ı başlat
python manage.py runserver
```

---

## ⚙️ Yapılandırma

### Environment Variables (.env)

`.env` dosyası projenin root dizininde bulunur ve aşağıdaki değişkenleri içerir:

#### Django Ayarları

```bash
# Django Secret Key (GÜVENLİK İÇİN ÖNEMLİ!)
SECRET_KEY=super-secret-key

# Debug modu (Production'da False yapın!)
DEBUG=True

# İzin verilen host'lar (virgülle ayrılmış)
ALLOWED_HOSTS=127.0.0.1,localhost
```

#### Veritabanı Ayarları

```bash
# SQLite (varsayılan)
DATABASE_URL=sqlite:///db.sqlite3

# PostgreSQL örneği (isteğe bağlı)
# DATABASE_URL=postgres://user:password@localhost:5432/kitti_db
```

#### Admin Kullanıcı Ayarları

```bash
# Django Superuser bilgileri
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin123
DJANGO_SUPERUSER_EMAIL=admin@example.com
```

#### Şifreleme Ayarları

```bash
# Fernet key (django-cryptography için)
FERNET_KEY=e8s4gyWp10mHXMFKOTWG3ALmWcq2Q0UOaxsR30ebiBE=
```

**Not:** Production ortamında yeni bir FERNET_KEY oluşturun:
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

#### Email Ayarları

```bash
# Email backend
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

# SMTP sunucu ayarları
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True

# Email hesap bilgileri
EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=your-app-password-here

# Alıcı email adresi
RECIEPENT_EMAIL=example@gmail.com
```

**Gmail için App Password:**
1. Google hesabınıza giriş yapın
2. Güvenlik > 2 Adımlı Doğrulama'yı etkinleştirin
3. Uygulama şifreleri > Yeni uygulama şifresi oluşturun
4. Oluşturulan şifreyi `EMAIL_HOST_PASSWORD` alanına yapıştırın

---

## 🎯 Kullanım

### Hızlı Başlangıç

```bash
# Projeyi başlat
python manage.py run

# Örnek veri ile başlat
python manage.py run --fake-data

# Tarayıcıyı otomatik aç
python manage.py run --open-browser

# Özel port ile başlat
python manage.py run --port 8080
```

### Komut Seçenekleri

```bash
# Temel başlatma
python manage.py run

# Örnek veri ile başlat
python manage.py run --fake-data

# Örnek veri sayılarını ayarla
python manage.py run --fake-data --categories 20 --sliders 5

# Mevcut örnek veriyi temizle ve yeniden oluştur
python manage.py run --fake-data --clear-data

# Static dosyaları toplamadan başlat (hızlı)
python manage.py run --skip-static

# Migration'ları atla (development)
python manage.py run --skip-migrate --skip-static

# Server'ı başlatmadan sadece setup yap
python manage.py run --no-server

# Tarayıcıyı otomatik aç
python manage.py run --open-browser
```

### Admin Paneline Erişim

1. Server'ı başlatın: `python manage.py run`
2. Tarayıcıda açın: `http://127.0.0.1:8000/admin/`
3. Giriş yapın:
   - **Kullanıcı Adı**: `admin`
   - **Şifre**: `admin123`

### API Endpoint'lerine Erişim

- **API Ana Sayfa**: `http://127.0.0.1:8000/api/`
- **Swagger Dokümantasyon**: `http://127.0.0.1:8000/api/docs/swagger/`
- **ReDoc Dokümantasyon**: `http://127.0.0.1:8000/api/docs/redoc/`
- **OpenAPI Schema**: `http://127.0.0.1:8000/api/schema/`

---

## 📚 API Dokümantasyonu

### Temel Endpoint'ler

#### 1. Kategoriler

**GET** `/api/categories/`

Kategorileri ve alt ürünlerini listeler.

**Query Parametreleri:**
- `lang` (tr/en): Dil seçimi
- `category_type` (type1/type2/type3/type4/type5): Kategori tipi
- `search`: Arama terimi
- `ordering`: Sıralama (lft, level, id)

**Örnek:**
```bash
# Türkçe kategoriler
curl http://127.0.0.1:8000/api/categories/?lang=tr

# İngilizce kategoriler
curl http://127.0.0.1:8000/api/categories/?lang=en

# Belirli tip kategoriler
curl http://127.0.0.1:8000/api/categories/?category_type=type1
```

#### 2. Ürünler

**GET** `/api/products/`

Tüm ürünleri listeler.

**Query Parametreleri:**
- `lang` (tr/en): Dil seçimi
- `category`: Kategori ID filtresi
- `search`: Arama terimi
- `ordering`: Sıralama (id, lft)

**Örnek:**
```bash
# Tüm ürünler (Türkçe)
curl http://127.0.0.1:8000/api/products/?lang=tr

# Belirli kategorideki ürünler
curl http://127.0.0.1:8000/api/products/?category=1

# Ürün arama
curl http://127.0.0.1:8000/api/products/?search=laptop
```

#### 3. Slider'lar

**GET** `/api/sliders/`

Slider öğelerini listeler.

**Query Parametreleri:**
- `lang` (tr/en): Dil seçimi

**Örnek:**
```bash
curl http://127.0.0.1:8000/api/sliders/?lang=tr
```

### API Özellikleri

- 🔍 **Arama ve Filtreleme**: Ürünleri isme göre arayın, kategoriye göre filtreleyin
- 🌐 **Çok Dilli**: `?lang=tr` veya `?lang=en` parametresi kullanın
- 📄 **Sayfalama**: Büyük veri setleri için otomatik sayfalama (sayfa başına 20 öğe)
- 📝 **Dokümantasyon**: Tam Swagger/OpenAPI dokümantasyonu

### API Response Formatı

```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Ürün Adı",
      "description": "Ürün Açıklaması",
      "icon": "http://127.0.0.1:8000/media/item_icons/icon.png",
      "images": [
        {
          "id": 1,
          "image": "http://127.0.0.1:8000/media/item_images/image1.png"
        }
      ],
      "level": 1,
      "lft": 1,
      "rght": 2
    }
  ]
}
```

---

## 📁 Proje Yapısı

```
kitti-backend/
├── 📁 contacts/              # İletişim modülü
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── 📁 kitti/                 # Ana Django projesi
│   ├── settings/
│   │   └── base.py           # Ana ayar dosyası
│   ├── urls.py               # Ana URL yapılandırması
│   ├── wsgi.py
│   └── asgi.py
│
├── 📁 products/              # Ürün yönetim modülü
│   ├── models.py             # Item, ItemImage, Slider modelleri
│   ├── views.py              # API view'ları
│   ├── serializers.py        # API serializer'ları
│   ├── admin.py              # Admin panel yapılandırması
│   ├── urls.py               # URL routing
│   ├── translation.py        # Çeviri ayarları
│   └── management/
│       └── commands/
│           ├── run.py                    # Ana başlatma komutu
│           ├── create_default_superuser.py
│           └── create_fake_data.py
│
├── 📁 site_settings/         # Site ayarları modülü
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── 📁 staticfiles/           # Static dosyalar
│   ├── admin/
│   │   └── images/
│   │       └── kitti-logo.svg
│   └── fake_data/
│       ├── product_image/    # Örnek ürün görselleri
│       └── slider/          # Örnek slider görselleri
│
├── 📁 media/                 # Yüklenen dosyalar
│   ├── item_images/         # Ürün görselleri
│   ├── item_icons/          # Ürün ikonları
│   ├── sliders/             # Slider görselleri
│   └── site/                # Site görselleri
│
├── 📁 venv/                 # Virtual environment (git'e eklenmez)
│
├── 📄 .env                   # Environment değişkenleri (GÜVENLİ!)
├── 📄 .env-example           # Environment şablonu
├── 📄 .gitignore             # Git ignore kuralları
├── 📄 requirements.txt       # Python bağımlılıkları
├── 📄 manage.py              # Django yönetim scripti
├── 📄 db.sqlite3             # SQLite veritabanı (git'e eklenmez)
└── 📄 README.md              # Bu dosya
```

### Model Yapısı

#### Item Modeli
- **item_type**: `category` veya `product`
- **title**: Başlık (TR/EN)
- **description**: Açıklama (TR/EN)
- **icon**: Kategori/ürün ikonu
- **category_type**: Kategori görünüm tipi (type1-type5)
- **parent**: MPTT parent referansı
- **children**: Alt kategoriler/ürünler

#### ItemImage Modeli
- **item**: Item referansı
- **image**: Ürün görseli

#### Slider Modeli
- **title**: Başlık (TR/EN)
- **image**: Slider görseli (TR/EN)
- **parent**: MPTT parent (sıralama için)

---

## 🛠️ Geliştirme

### Yeni Migration Oluşturma

```bash
# Model değişikliklerinden sonra
python manage.py makemigrations

# Migration'ları uygula
python manage.py migrate
```

### Yeni Admin Kullanıcısı Oluşturma

```bash
python manage.py createsuperuser
```

veya mevcut komutu kullanın:

```bash
python manage.py create_default_superuser
```

### Örnek Veri Oluşturma

```bash
# Varsayılan örnek veri
python manage.py create_fake_data

# Özel sayılarla
python manage.py create_fake_data --categories 20 --sliders 5

# Mevcut veriyi temizle
python manage.py create_fake_data --clear
```

### Static Dosyaları Toplama

```bash
python manage.py collectstatic --noinput
```

### Çeviri Dosyalarını Güncelleme

```bash
# Çeviri dosyalarını oluştur
python manage.py makemessages -l en
python manage.py makemessages -l tr

# Çeviri dosyalarını derle
python manage.py compilemessages
```

---

## 🆘 Sorun Giderme

### Port Zaten Kullanımda

**Sorun:** `Error: That port is already in use`

**Çözüm:**
```bash
# Farklı bir port kullan
python manage.py run --port 8080

# veya kullanan process'i bul ve durdur
# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Veritabanı Hataları

**Sorun:** Migration hataları veya veritabanı bozuk

**Çözüm:**
```bash
# Veritabanını sıfırla (DİKKAT: Tüm veri silinir!)
rm db.sqlite3
python manage.py migrate
python manage.py create_default_superuser
```

### Static Dosyalar Yüklenmiyor

**Sorun:** CSS/JS dosyaları görünmüyor

**Çözüm:**
```bash
# Static dosyaları yeniden topla
python manage.py collectstatic --noinput

# veya skip-static ile başlat (development için)
python manage.py run --skip-static
```

### Import Hataları

**Sorun:** `ModuleNotFoundError` veya import hataları

**Çözüm:**
```bash
# Virtual environment'ı aktif ettiğinizden emin olun
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate    # Windows

# Bağımlılıkları yeniden yükleyin
pip install -r requirements.txt
```

### Email Gönderim Sorunları

**Sorun:** Email gönderilemiyor

**Çözüm:**
1. `.env` dosyasındaki email ayarlarını kontrol edin
2. Gmail kullanıyorsanız App Password kullandığınızdan emin olun
3. `EMAIL_USE_TLS=True` olduğundan emin olun
4. Firewall/antivirus yazılımının SMTP portunu engellemediğinden emin olun

### Admin Panel'e Giriş Yapılamıyor

**Sorun:** Admin kullanıcısı yok veya şifre hatırlanmıyor

**Çözüm:**
```bash
# Yeni admin kullanıcısı oluştur
python manage.py create_default_superuser

# veya manuel oluştur
python manage.py createsuperuser
```

### CORS Hataları

**Sorun:** API'ye frontend'den erişilemiyor

**Çözüm:**
`kitti/settings/base.py` dosyasında CORS ayarları zaten yapılandırılmış:
```python
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
```

Eğer hala sorun varsa, `ALLOWED_HOSTS` değişkenine frontend domain'ini ekleyin.

---

## 🔐 Güvenlik Notları

### Production Ortamı İçin

1. **SECRET_KEY**: Mutlaka güçlü, rastgele bir key kullanın
2. **DEBUG**: `False` yapın
3. **ALLOWED_HOSTS**: Sadece izin verilen domain'leri ekleyin
4. **HTTPS**: SSL sertifikası kullanın
5. **Veritabanı**: SQLite yerine PostgreSQL kullanın
6. **FERNET_KEY**: Yeni bir key oluşturun
7. **Email Şifreleri**: App Password kullanın, normal şifre değil

### .env Dosyası Güvenliği

- ✅ Repo private olduğu için `.env` dosyası güvenli
- ⚠️ Production'da `.env` dosyasını asla public repo'ya commit etmeyin
- ✅ `.gitignore` dosyasında `.env` zaten ignore edilmiş (ancak force add ile eklenmiş)

---

## 📊 Veritabanı Yapısı

### SQLite (Varsayılan)

- **Dosya**: `db.sqlite3`
- **Konum**: Proje root dizini
- **Kullanım**: Development ve küçük projeler için

### PostgreSQL (Production)

`.env` dosyasında:
```bash
DATABASE_URL=postgres://user:password@localhost:5432/kitti_db
```

`requirements.txt`'e ekleyin:
```
psycopg2-binary==2.9.9
```

---

## 🎨 Admin Panel Özellikleri

### Jazzmin Admin Paneli

- Modern ve kullanıcı dostu arayüz
- Özelleştirilebilir menü yapısı
- İkon desteği
- Responsive tasarım
- Dark mode desteği

### Admin Panel Özellikleri

- Kategori ve ürün yönetimi
- Hiyerarşik yapı görünümü (MPTT)
- Çoklu dil desteği
- Görsel yükleme ve yönetimi
- Slider yönetimi
- Site ayarları yönetimi

---

## 📝 Lisans

**BOSOFT Kitti Platform** - Professional Product Management System

---

## 💼 Destek

### Yardım İçin

- 📧 **Email**: BOSOFT Support
- 📖 **Dokümantasyon**: `/api/docs/` (server çalışırken)
- 🐛 **Hata Bildirimi**: Repository'de issue oluşturun

---

<div align="center">

**💼 Made with ❤️ by BOSOFT**

*Excellence in Software Development*

[![BOSOFT](https://img.shields.io/badge/BOSOFT-Professional%20Software%20Solutions-red.svg?style=for-the-badge)](https://bionluk.com/bologo)

https://bionluk.com/orders/2191240 iş teslimidir.

</div>

---

## 📌 Hızlı Referans

### En Çok Kullanılan Komutlar

```bash
# Projeyi başlat
python manage.py run

# Örnek veri ile başlat
python manage.py run --fake-data

# Migration oluştur
python manage.py makemigrations

# Migration uygula
python manage.py migrate

# Admin kullanıcısı oluştur
python manage.py create_default_superuser

# Static dosyaları topla
python manage.py collectstatic --noinput

# Server'ı başlat
python manage.py runserver
```

### Önemli URL'ler

- Admin: `http://127.0.0.1:8000/admin/`
- API Docs: `http://127.0.0.1:8000/api/docs/swagger/`
- Categories: `http://127.0.0.1:8000/api/categories/`
- Products: `http://127.0.0.1:8000/api/products/`
- Sliders: `http://127.0.0.1:8000/api/sliders/`

### Varsayılan Kullanıcı Bilgileri

- **Kullanıcı Adı**: `admin`
- **Şifre**: `admin123`
- **Email**: `admin@example.com`

---

**Son Güncelleme**: 2025
