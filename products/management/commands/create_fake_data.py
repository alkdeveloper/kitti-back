# products/management/commands/create_fake_data.py
import os
import random
import shutil
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from products.models import Item, ItemImage, Slider
from faker import Faker

class Command(BaseCommand):
    help = 'Creates fake data for categories, products, and sliders'
    
    def __init__(self):
        super().__init__()
        self.fake = Faker(['tr_TR'])  # Türkçe fake data
        self.fake_en = Faker(['en_US'])  # İngilizce fake data
        
    def add_arguments(self, parser):
        parser.add_argument(
            '--categories',
            type=int,
            default=10,
            help='Number of categories to create (default: 10)'
        )
        parser.add_argument(
            '--sliders',
            type=int,
            default=3,
            help='Number of sliders to create (default: 3)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new ones'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(
                self.style.WARNING('Clearing existing data...')
            )
            Item.objects.all().delete()
            Slider.objects.all().delete()
            
        self.create_categories(options['categories'])
        self.create_sliders(options['sliders'])
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {options['categories']} categories with products "
                f"and {options['sliders']} sliders"
            )
        )

    def create_categories(self, count):
        """Kategoriler ve altındaki ürünleri oluştur"""
        self.stdout.write('Creating categories and products...')
        
        category_types = ['type1', 'type2', 'type3', 'type4']
        
        for i in range(count):
            # Kategori oluştur
            category = Item.objects.create(
                title_tr=f"Kategori {i+1} - {self.fake.word().title()}",
                title_en=f"Category {i+1} - {self.fake_en.word().title()}",
                description_tr=self.fake.text(max_nb_chars=200),
                description_en=self.fake_en.text(max_nb_chars=200),
                item_type='category',
                category_type=random.choice(category_types)
            )
            
            # Kategori için icon ekle
            self.add_category_icon(category)
            
            # Her kategoriye 5-10 arası ürün ekle
            product_count = random.randint(5, 10)
            for j in range(product_count):
                product = Item.objects.create(
                    title_tr=f"{self.fake.catch_phrase()} {j+1}",
                    title_en=f"{self.fake_en.catch_phrase()} {j+1}",
                    description_tr=self.fake.text(max_nb_chars=300),
                    description_en=self.fake_en.text(max_nb_chars=300),
                    item_type='product',
                    parent=category
                )
                
                # Ürün için icon ekle
                self.add_product_icon(product)
                
                # Ürün için 1-3 arası resim ekle
                image_count = random.randint(1, 3)
                for k in range(image_count):
                    self.add_product_image(product)
            
            self.stdout.write(f'✓ Category {i+1} created with {product_count} products')

    def create_sliders(self, count):
        """Slider'ları oluştur"""
        self.stdout.write('Creating sliders...')
        
        for i in range(count):
            slider = Slider.objects.create(
                title_tr=f"Slider {i+1} - {self.fake.sentence(nb_words=4)}",
                title_en=f"Slider {i+1} - {self.fake_en.sentence(nb_words=4)}"
            )
            
            # Slider için resim ekle (hem TR hem EN)
            self.add_slider_images(slider)
            
            self.stdout.write(f'✓ Slider {i+1} created')

    def add_category_icon(self, category):
        """Kategoriye random icon ekle"""
        try:
            # Basit renkli placeholder oluştur veya varsayılan resim kullan
            pass  # Bu örnekte icon eklemeyi atlıyoruz
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not add icon to category: {e}')
            )

    def add_product_icon(self, product):
        """Ürüne random icon ekle"""
        try:
            product_images_dir = os.path.join(
                settings.BASE_DIR, 'static', 'fake_data', 'product_images'
            )
            
            if os.path.exists(product_images_dir):
                images = [f for f in os.listdir(product_images_dir) 
                         if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                
                if images:
                    random_image = random.choice(images)
                    source_path = os.path.join(product_images_dir, random_image)
                    
                    # Media klasörüne kopyala
                    media_dir = os.path.join(settings.MEDIA_ROOT, 'item_icons')
                    os.makedirs(media_dir, exist_ok=True)
                    
                    new_filename = f"product_icon_{product.id}_{random_image}"
                    dest_path = os.path.join(media_dir, new_filename)
                    
                    shutil.copy2(source_path, dest_path)
                    product.icon.name = f'item_icons/{new_filename}'
                    product.save()
                    
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not add icon to product: {e}')
            )

    def add_product_image(self, product):
        """Ürüne random resim ekle"""
        try:
            product_images_dir = os.path.join(
                settings.BASE_DIR, 'static', 'fake_data', 'product_images'
            )
            
            if os.path.exists(product_images_dir):
                images = [f for f in os.listdir(product_images_dir) 
                         if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                
                if images:
                    random_image = random.choice(images)
                    source_path = os.path.join(product_images_dir, random_image)
                    
                    # Media klasörüne kopyala
                    media_dir = os.path.join(settings.MEDIA_ROOT, 'item_images')
                    os.makedirs(media_dir, exist_ok=True)
                    
                    new_filename = f"product_{product.id}_{random.randint(1000, 9999)}_{random_image}"
                    dest_path = os.path.join(media_dir, new_filename)
                    
                    shutil.copy2(source_path, dest_path)
                    
                    # ItemImage oluştur
                    item_image = ItemImage.objects.create(item=product)
                    item_image.image.name = f'item_images/{new_filename}'
                    item_image.save()
                    
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not add image to product: {e}')
            )

    def add_slider_images(self, slider):
        """Slider'a hem TR hem EN resim ekle"""
        try:
            slider_images_dir = os.path.join(
                settings.BASE_DIR, 'static', 'fake_data', 'sliders'
            )
            
            if os.path.exists(slider_images_dir):
                images = [f for f in os.listdir(slider_images_dir) 
                         if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                
                if images:
                    # TR resmi
                    random_image_tr = random.choice(images)
                    self.copy_slider_image(slider, random_image_tr, 'tr')
                    
                    # EN resmi (farklı olabilir)
                    random_image_en = random.choice(images)
                    self.copy_slider_image(slider, random_image_en, 'en')
                    
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not add images to slider: {e}')
            )

    def copy_slider_image(self, slider, image_name, lang):
        """Slider resmi kopyala"""
        try:
            source_path = os.path.join(
                settings.BASE_DIR, 'static', 'fake_data', 'sliders', image_name
            )
            
            # Media klasörüne kopyala
            media_dir = os.path.join(settings.MEDIA_ROOT, 'sliders')
            os.makedirs(media_dir, exist_ok=True)
            
            new_filename = f"slider_{slider.id}_{lang}_{image_name}"
            dest_path = os.path.join(media_dir, new_filename)
            
            shutil.copy2(source_path, dest_path)
            
            # Dile göre field'ı set et
            if lang == 'tr':
                slider.image_tr.name = f'sliders/{new_filename}'
            else:
                slider.image_en.name = f'sliders/{new_filename}'
            
            slider.save()
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not copy slider image: {e}')
            )