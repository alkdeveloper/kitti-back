from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from site_settings.models import (
    SiteSettings, MenuItem, Header, GenericSection, FooterPolicy,
    SocialMedia, FooterInfo
)
import os
from django.core.files import File

class Command(BaseCommand):
    help = "Creates default site settings with multilingual dummy data and images."

    def handle(self, *args, **kwargs):
        # === 1️⃣ Site Settings ===
        site, created = SiteSettings.objects.get_or_create(
            site_title="Kitti",
            site_description="<b>Hoş geldiniz!</b> Kitti dünyasına adım atın.",
        )

        static_path = os.path.join("static/site_data", "logo.svg")
            
        if os.path.exists(static_path):
            with open(static_path, 'rb') as f:
                # Modelin image alanına kaydet
                site.logo.save("logo.svg", File(f), save=True)
        else:
            print(f"Dosya bulunamadı: {static_path}")

        # === 2️⃣ Menü ===
        menu_items = [
            {"href": "/", "text_tr": "Anasayfa", "text_en": "Home"},
            {"href": "/products", "text_tr": "Ürünler", "text_en": "Products"},
            {"href": "/our-story", "text_tr": "Hikayemiz", "text_en": "Our Story"},
            {"href": "/contact", "text_tr": "İletişim", "text_en": "Contact"},
            {"href": "/toptan-portal", "text_tr": "Toptan Portal", "text_en": "Wholesale Portal"},
        ]
        for item in menu_items:
            MenuItem.objects.get_or_create(site=site, **item)

        # === 3️⃣ Görsel yolu yardımcı fonksiyonu ===
        def add_image_to_section(section, filename):
            """
            Statik dosyayı alıp modelin ImageField'ine kaydeder.
            """
            # Statik dosya yolu
            static_path = os.path.join("static/site_data", filename)
            
            if os.path.exists(static_path):
                with open(static_path, 'rb') as f:
                    # Modelin image alanına kaydet
                    section.image.save(filename, File(f), save=True)
            else:
                print(f"Dosya bulunamadı: {static_path}")

        # === 4️⃣ Header ===
        header_1, created_1 = Header.objects.get_or_create(
            site=site,
            title_tr="Doğallığın Gücü",
            title_en="The Power of Nature",
            description_tr="<b>Kitti</b> ile doğallığın gücü.",
            description_en="<b>Kitti</b> with the power of nature.",
        )
        if created_1:
            add_image_to_section(header_1, "header_1.gif")

        header_2, created_2 = Header.objects.get_or_create(
            site=site,
            title_tr="Sürdürülebilir Ürünler",
            title_en="Sustainable Products",
            description_tr="Sürdürülebilir ürünlerle geleceğe yatırım.",
            description_en="Investing in the future with sustainable products.",
        )
        if created_2:
            add_image_to_section(header_2, "header_2.gif")

        header_3, created_3 = Header.objects.get_or_create(
            site=site,
            title_tr="header 3",
            title_en="header 3",
            description_tr="header 3.",
            description_en="header 3",
        )
        if created_3:
            add_image_to_section(header_3, "header_3.png")

        # WhatsKitty Section
        section_1, created_3 = GenericSection.objects.get_or_create(
            site=site,
            type='whats_kitty',
            defaults={
                'name': "What's Kitty",
                'title_tr': "Kitti Nedir?",
                'title_en': "What is Kitti?",
                'description_tr': "Kitti, 1978'den beri tekstil sektöründe faaliyet gösteren ALK Group'un markalarından biridir.\n\nALK Group; Kitti gibi birçok markasıyla hem Türkiye'de hem dünyada milyonlara ulaşır.",
                'description_en': "Kitti is one of the brands of ALK Group, active in the textile industry since 1978.\n\nWith many brands like Kitti, ALK Group reaches millions both in Turkey and around the world.",
                'button_text_left_tr': "Ürünleri İncele",
                'button_text_left_en': "Explore Products",
                'button_url_left': '/contact/',
            },
        )
        if created_3:
            add_image_to_section(section_1, "section_1.png")

        # Favorites of the Season Section
        GenericSection.objects.get_or_create(
            site=site,
            type='favorites_of_season',
            defaults={
                'name': "Favoriler",
                'title_tr': "Sezonun Favorileri",
                'title_en': "Season Favorites",
                'description_tr': "Sezonun en sevilen çocuk aksesuarlarını tasarlar, üretir ve Türkiye'nin dört bir yanına ulaştırırız.",
                'description_en': "We design, produce, and distribute the most loved children's accessories of the season across Turkey.",
                'button_text_left_tr': "Ve daha onlarca kategoriyi inceleyin",
                'button_text_left_en': "Explore dozens of other categories",
                'button_url_left': '/products/',
            },
        )

        # Who Are We
        section_3, created_4 = GenericSection.objects.get_or_create(
            site=site,
            type='who_are_we',
            defaults={
                'name':"Who Are We?",
                'subtitle_tr':"Atölyeden Dünyaya",
                'subtitle_en':"From the Workshop to the World",
                'title_tr':"Biz Kimiz?",
                'title_en':"Who Are We?",
                'description_tr':"Kitti, 1978'den beri tekstil sektöründe faaliyet gösteren ALK Group'un markalarından biridir.",
                'description_en':"Kitti has been part of ALK Group, a textile leader since 1978.",
            },
        )
        if created_4:
            add_image_to_section(section_3, "section_3.gif")

        # Who Are We
        section_4, created_5 = GenericSection.objects.get_or_create(
            site=site,
            type='from_the_workshop',
            defaults={
                'name':"From the Workshop",
                'subtitle_tr':"Atölyeden Dünyaya",
                'subtitle_en':"From the Workshop to the World",
                'title_tr':"GÜÇLÜ ÜRETİM KAPASİTESİ",
                'title_en':"STRONG PRODUCTION CAPACITY",
                'description_tr':"Kitti, 2.000 adetten milyonlarca adede ulaşan üretim kapasitesiyle farklı pazarlara hizmet veriyor. %50 çocuk, %30 erkek, %20 kadın aksesuarlarından oluşan koleksiyonlarımız; İngiltere, Sırbistan, Rusya ve daha bir çok ülkeye ihraç ediliyor.",
                'description_en':"Kitti serves diverse markets with a production capacity ranging from 2,000 to millions of units. Our collections, comprised of 50% children's, 30% men's, and 20% women's accessories, are exported to the UK, Serbia, Russia, and many other countries.",
            },
        )
        if created_5:
            add_image_to_section(section_4, "section_4.gif")

        # Its Story
        section_5, created_6 = GenericSection.objects.get_or_create(
            site=site,
            type='its_story',
            defaults={
                'name':"Its Story",
                'subtitle_tr':"1978'den bu güne",
                'subtitle_en':"Since 1978",
                'title_tr':"Kitti Hikayesi",
                'title_en':"The Kitti Story",
                'description_tr':"Minik kafalar için büyük bir hikaye yazıyoruz. Her ürünümüzde kalite, güvenlik ve sevgi var.",
                'description_en':"We’re writing a big story for little heads — filled with quality, safety, and love.",
            },
        )
        if created_6:
            add_image_to_section(section_5, "section_5.png")

        # Production Capacity
        section_6, created_7 = GenericSection.objects.get_or_create(
            site=site,
            type='production_capacity',
            defaults={
                'name':"Production Capacity",
                'subtitle_tr':"Sipariş sürecini kolaylaştırıyoruz",
                'subtitle_en':"Simplifying the Order Process",
                'title_tr':"Üretim Kapasitemiz",
                'title_en':"Our Production Capacity",
                'description_tr':"Modern tesislerimizde günlük binlerce ürün üretiyoruz. Kaliteli hammaddeler ve uzman ekibimizle en iyisini sunuyoruz.",
                'description_en':"We produce thousands of products daily in modern facilities with top-quality materials.",
                'button_text_left_tr':"Detayları Gör",
                'button_text_left_en':"See Details",
                'button_url_left':"/contacts",
                'button_text_right_tr':"Ürün Kataloğu",
                'button_text_right_en':"Product Catalog",
                'button_url_right':"/products",
            },
        )
        if created_7:
            add_image_to_section(section_6, "section_6.png")

        # === 8️⃣ Footer Policies ===
        footer_policies = [
            {"title_tr": "Aydınlatma Metni", "title_en": "Information Text"},
            {"title_tr": "İleti Onay Metni", "title_en": "Message Consent Text"},
            {"title_tr": "Çerez Politikası", "title_en": "Cookie Policy"},
        ]
        for policy in footer_policies:
            FooterPolicy.objects.get_or_create(site=site, **policy)

        # === 9️⃣ Sosyal Medya ===
        SocialMedia.objects.get_or_create(site=site, icon="facebook", url="https://facebook.com")
        SocialMedia.objects.get_or_create(site=site, icon="instagram", url="https://instagram.com")

        # === 🔟 Footer Info ===
        FooterInfo.objects.get_or_create(site=site)

        self.stdout.write(self.style.SUCCESS("✅ Default multilingual site settings created successfully with images."))
