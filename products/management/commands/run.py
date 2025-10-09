import os
import subprocess
import threading
import time
import webbrowser
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.contrib.auth.models import User
from products.models import Item, Slider

class Command(BaseCommand):
    help = 'BOSOFT Kitti Project - Complete setup and launch'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.port = 8000  # Default port
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--fake-data',
            action='store_true',
            help='Generate sample data (categories, products, sliders)'
        )
        parser.add_argument(
            '--categories',
            type=int,
            default=10,
            help='Number of categories to create (default: 10, only with --fake-data)'
        )
        parser.add_argument(
            '--sliders',
            type=int,
            default=3,
            help='Number of sliders to create (default: 3, only with --fake-data)'
        )
        parser.add_argument(
            '--skip-static',
            action='store_true',
            help='Skip collectstatic command'
        )
        parser.add_argument(
            '--skip-migrate',
            action='store_true',
            help='Skip migrations'
        )
        parser.add_argument(
            '--clear-data',
            action='store_true',
            help='Clear existing fake data before creating new ones (only with --fake-data)'
        )
        parser.add_argument(
            '--no-server',
            action='store_true',
            help='Don\'t start development server'
        )
        parser.add_argument(
            '--port',
            type=int,
            default=8000,
            help='Development server port (default: 8000)'
        )
        parser.add_argument(
            '--open-browser',
            action='store_true',
            help='Open browser automatically'
        )

    def handle(self, *args, **options):
        self.port = options['port']
        self.open_browser = options['open_browser']
        self.fake_data_requested = options['fake_data']
        
        self.print_banner()
        
        # 1. Check fake data directories (sadece fake-data istenirse)
        if self.fake_data_requested:
            self.check_fake_data_dirs()
        
        # 2. Run migrations
        if not options['skip_migrate']:
            if not self.run_migrations():
                return
        
        # 3. Collect static files
        if not options['skip_static']:
            self.collect_static()
        
        # 4. Create superuser
        self.create_superuser()

        call_command('create_default_site_settings')
        
        # 5. Create fake data (sadece istenirse ve henüz yoksa)
        if self.fake_data_requested:
            if self.should_create_fake_data(options):
                self.create_fake_data(options)
            else:
                self.stdout.write('ℹ️ Sample content already exists, skipping generation')
        else:
            self.stdout.write('ℹ️ Sample data generation skipped (use --fake-data to enable)')
        
        # 6. Final success message
        self.print_success()
        
        # 7. Start development server
        if not options['no_server']:
            self.start_server()

    def should_create_fake_data(self, options):
        """Fake data oluşturup oluşturmayacağına karar ver"""
        # Eğer clear-data istenirse her zaman oluştur
        if options['clear_data']:
            return True
        
        # Eğer hiç data yoksa oluştur
        has_items = Item.objects.exists()
        has_sliders = Slider.objects.exists()
        
        if not has_items and not has_sliders:
            return True
        
        # Data varsa oluşturma
        return False

    def print_banner(self):
        """BOSOFT başlangıç banner'ı"""
        banner = """
╔══════════════════════════════════════╗
║             🚀 BOSOFT 🚀             ║
║            KITTI LAUNCHER            ║
║        Professional Setup Tool       ║
╚══════════════════════════════════════╝
        """
        self.stdout.write(self.style.SUCCESS(banner))
        self.stdout.write(self.style.HTTP_INFO('💼 Powered by BOSOFT - Excellence in Software'))
        self.stdout.write()

    def check_fake_data_dirs(self):
        """Fake data klasörlerinin varlığını kontrol et"""
        self.stdout.write('📂 Checking project assets...')
        
        required_dirs = [
            os.path.join(settings.BASE_DIR, 'static', 'fake_data', 'product_images'),
            os.path.join(settings.BASE_DIR, 'static', 'fake_data', 'sliders'),
        ]
        
        missing_dirs = []
        for dir_path in required_dirs:
            if not os.path.exists(dir_path):
                missing_dirs.append(dir_path)
                os.makedirs(dir_path, exist_ok=True)
                self.stdout.write(f'📁 Created: {dir_path}')
        
        if not missing_dirs:
            self.stdout.write('✅ All project directories ready')
        
        # Check for images
        product_images_dir = required_dirs[0]
        slider_images_dir = required_dirs[1]
        
        try:
            product_images = [f for f in os.listdir(product_images_dir) 
                             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))] if os.path.exists(product_images_dir) else []
            
            slider_images = [f for f in os.listdir(slider_images_dir) 
                            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))] if os.path.exists(slider_images_dir) else []
        except (OSError, FileNotFoundError):
            product_images = []
            slider_images = []
        
        self.stdout.write(f'📷 Found {len(product_images)} product assets')
        self.stdout.write(f'🖼️ Found {len(slider_images)} banner assets')

    def run_migrations(self):
        """Migration'ları çalıştır"""
        self.stdout.write('🔄 Initializing database...')
        try:
            call_command('migrate', verbosity=0)
            self.stdout.write('✅ Database initialized successfully')
            return True
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Database initialization failed: {e}')
            )
            return False

    def collect_static(self):
        """Static dosyaları topla"""
        self.stdout.write('📁 Collecting static assets...')
        try:
            call_command('collectstatic', '--noinput', verbosity=0)
            self.stdout.write('✅ Static assets collected')
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Could not collect static assets: {e}')
            )

    def create_superuser(self):
        """Superuser oluştur"""
        self.stdout.write('👤 Setting up administrator account...')
        try:
            if User.objects.filter(username='admin').exists():
                self.stdout.write('ℹ️ Administrator account already exists')
            else:
                call_command('create_default_superuser')
                self.stdout.write('✅ Administrator account created')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Could not create administrator: {e}')
            )

    def create_fake_data(self, options):
        """Sample data oluştur"""
        self.stdout.write('🎭 Generating sample content...')
        try:
            cmd_options = {
                'categories': options['categories'],
                'sliders': options['sliders']
            }
            
            if options['clear_data']:
                cmd_options['clear'] = True
            
            call_command('create_fake_data', **cmd_options)
            self.stdout.write('✅ Sample content generated successfully')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Could not generate sample content: {e}')
            )

    def print_success(self):
        """BOSOFT başarı mesajı"""
        # Data durumunu kontrol et
        item_count = Item.objects.count()
        slider_count = Slider.objects.count()
        
        data_status = ""
        if item_count > 0 or slider_count > 0:
            data_status = f"""
📊 Current Data Status:
   📋 Categories & Products: {item_count} items
   🖼️ Sliders: {slider_count} items"""
        
        success_msg = f"""
╔══════════════════════════════════════╗
║        🎉 BOSOFT KITTI READY 🎉      ║
║         Project Launch Success       ║
╚══════════════════════════════════════╝

🌟 BOSOFT Kitti Platform is ready to launch!
{data_status}

🎯 Access Points:
   🔗 Admin Panel: http://127.0.0.1:{self.port}/admin/
   📚 API Docs:    http://127.0.0.1:{self.port}/api/docs/
   🔍 API Schema:  http://127.0.0.1:{self.port}/api/schema/
   📋 Categories:  http://127.0.0.1:{self.port}/api/categories/
   📦 Products:    http://127.0.0.1:{self.port}/api/products/
   🖼️ Sliders:     http://127.0.0.1:{self.port}/api/sliders/

👑 Admin Credentials:
   Username: admin
   Password: admin123

╔══════════════════════════════════════╗
║         💼 BOSOFT Quality ™          ║
╚══════════════════════════════════════╝
        """
        self.stdout.write(self.style.SUCCESS(success_msg))

    def start_server(self):
        """Server'ı başlat"""
        self.stdout.write('\n🚀 Launching BOSOFT Kitti Platform...')
        
        server_msg = f"""
╔══════════════════════════════════════╗
║         🌐 SERVER LAUNCHING 🌐       ║
║           BOSOFT Platform            ║
╚══════════════════════════════════════╝

🌍 Platform URL: http://127.0.0.1:{self.port}/
{f'🖥️ Browser will open automatically!' if self.open_browser else ''}

💡 BOSOFT Pro Tips:
   • Press Ctrl+C to stop the server
   • Server auto-reloads on code changes
   • All endpoints are documented in API docs
   • Use --fake-data to generate sample content

🎯 Quick Access:
   👉 Admin: http://127.0.0.1:{self.port}/admin/
   👉 API:   http://127.0.0.1:{self.port}/api/docs/

╔══════════════════════════════════════╗
║        💼 BOSOFT EXCELLENCE ™        ║
╚══════════════════════════════════════╝

Platform launching in 3 seconds...
        """
        self.stdout.write(self.style.SUCCESS(server_msg))
        
        # Düzeltilmiş geri sayım (loop'a girmez)
        for i in range(3, 0, -1):
            self.stdout.write(f'🚀 {i}...', ending='')
            self.stdout.flush()
            time.sleep(1)
        
        self.stdout.write('\n🎬 BOSOFT Kitti Platform is now LIVE!\n')
        
        # Browser'ı açmak için thread kullan (eğer istenirse)
        if self.open_browser:
            def open_browser_delayed():
                time.sleep(3)  # Server'ın başlamasını bekle
                try:
                    self.stdout.write('🌐 Opening browser...')
                    webbrowser.open(f'http://127.0.0.1:{self.port}/admin/')
                    time.sleep(1)
                    webbrowser.open(f'http://127.0.0.1:{self.port}/api/docs/')
                    self.stdout.write('✅ Browser opened successfully')
                except Exception as e:
                    self.stdout.write(f'⚠️ Could not open browser: {e}')
            
            browser_thread = threading.Thread(target=open_browser_delayed)
            browser_thread.daemon = True
            browser_thread.start()
        
        # Server'ı başlat
        try:
            self.stdout.write('╔══════════════════════════════════════╗')
            self.stdout.write('║    🚀 BOSOFT KITTI SERVER LIVE 🚀   ║')
            self.stdout.write('╚══════════════════════════════════════╝\n')
            call_command('runserver', f'127.0.0.1:{self.port}')
        except KeyboardInterrupt:
            goodbye_msg = """
╔══════════════════════════════════════╗
║           👋 BOSOFT KITTI            ║
║         Server Stopped Safely       ║
╚══════════════════════════════════════╝

Thank you for using BOSOFT Kitti Platform!
💼 BOSOFT - Excellence in Software Development
            """
            self.stdout.write(self.style.SUCCESS(goodbye_msg))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Server failed to start: {e}')
            )
            self.stdout.write('💼 Contact BOSOFT support for assistance')