from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from site_settings.models import (
    SiteSettings, MenuItem, Header, GenericSection, FooterPolicy,
    SocialMedia, FooterInfo, GenericSectionOurStory,
    GenericSectionContact, ContactAddresses, ContactMails, GenericSectionWholesale 
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

        # === 3️⃣ Görsel yolu yardımcı fonksiyonları ===
        def add_image_to_instance(instance, filename, field_name='image'):
            static_path = os.path.join("static/site_data", filename)
            if os.path.exists(static_path):
                with open(static_path, 'rb') as f:
                    image_field = getattr(instance, field_name)
                    image_field.save(filename, File(f), save=True)
            else:
                self.stdout.write(self.style.WARNING(f"Görsel dosyası bulunamadı: {static_path}"))

        # === 4️⃣ Header Bölümü (Yeniden Düzenlendi) ===
        headers_data = [
            {
                'unique_field': {'title_tr': "Header 1"},
                'defaults': {
                    'title_en': "Header 1",
                    'description_tr': "Header 1",
                    'description_en': "Header 1",
                },
                'image': 'header_1.gif'
            },
            {
                'unique_field': {'title_tr': "Header 2"},
                'defaults': {
                    'title_en': "Header 2",
                    'description_tr': "Header 2",
                    'description_en': "Header 2",
                },
                'image': 'header_2.gif'
            },
            {
                'unique_field': {'title_tr': "Header 3"},
                'defaults': {
                    'title_en': "Header 3",
                    'description_tr': "Header 3.",
                    'description_en': "Header 3",
                },
                'image': 'header_3.png'
            }
        ]

        for data in headers_data:
            header_obj, created = Header.objects.get_or_create(
                site=site,
                **data['unique_field'],
                defaults=data['defaults']
            )
            if created:
                if 'image' in data:
                    add_image_to_instance(header_obj, data['image'])
                self.stdout.write(self.style.SUCCESS(f"✅ Header '{data['unique_field']['title_tr']}' created."))

        # === 5️⃣ Ana Sayfa Genel Bölümleri (GenericSection - Yeniden Düzenlendi) ===
        generic_sections_data = [
            {
                'type': 'whats_kitty',
                'defaults': {
                    'name': "What's Kitty",
                    'title_tr': "Kitti Nedir?",
                    'title_en': "What is Kitti?",
                    'description_tr': "Kitti, 1978'den beri tekstil sektöründe faaliyet gösteren ALK Group'un markalarından biridir.\n\nALK Group; Kitti gibi birçok markasıyla hem Türkiye'de hem dünyada milyonlara ulaşır.",
                    'description_en': "Kitti is one of the brands of ALK Group, active in the textile industry since 1978.\n\nWith many brands like Kitti, ALK Group reaches millions both in Turkey and around the world.",
                    'button_text_left_tr': "Ürünleri İncele",
                    'button_text_left_en': "Explore Products",
                    'button_url_left': '/contact/',
                },
                'image': 'section_1.png',
                'mobile_image': 'section_1_mobile.png'
            },
            {
                'type': 'favorites_of_season',
                'defaults': {
                    'name': "Favorites",
                    'title_tr': "Sezonun Favorileri",
                    'title_en': "Season Favorites",
                    'description_tr': "Sezonun en sevilen çocuk aksesuarlarını tasarlar, üretir ve Türkiye'nin dört bir yanına ulaştırırız.",
                    'description_en': "We design, produce, and distribute the most loved children's accessories of the season across Turkey.",
                    'button_text_left_tr': "Ve daha onlarca kategoriyi inceleyin",
                    'button_text_left_en': "Explore dozens of other categories",
                    'button_url_left': '/products/',
                }
            },
            {
                'type': 'who_are_we',
                'defaults': {
                    'name': "Who Are We?",
                    'subtitle_tr': "Atölyeden Dünyaya",
                    'subtitle_en': "From the Workshop to the World",
                    'title_tr': "Biz Kimiz?",
                    'title_en': "Who Are We?",
                    'description_tr': "Kitti, 1978'den beri tekstil sektöründe faaliyet gösteren ALK Group'un markalarından biridir.",
                    'description_en': "Kitti has been part of ALK Group, a textile leader since 1978.",
                },
                'image': 'section_3.gif'
            },
            {
                'type': 'from_the_workshop',
                'defaults': {
                    'name': "From the Workshop",
                    'subtitle_tr': "Atölyeden Dünyaya",
                    'subtitle_en': "From the Workshop to the World",
                    'title_tr': "GÜÇLÜ ÜRETİM KAPASİTESİ",
                    'title_en': "STRONG PRODUCTION CAPACITY",
                    'description_tr': "Kitti, 2.000 adetten milyonlarca adede ulaşan üretim kapasitesiyle farklı pazarlara hizmet veriyor. %50 çocuk, %30 erkek, %20 kadın aksesuarlarından oluşan koleksiyonlarımız; İngiltere, Sırbistan, Rusya ve daha bir çok ülkeye ihraç ediliyor.",
                    'description_en': "Kitti serves diverse markets with a production capacity ranging from 2,000 to millions of units. Our collections, comprised of 50% children's, 30% men's, and 20% women's accessories, are exported to the UK, Serbia, Russia, and many other countries.",
                },
                'image': 'section_4.gif'
            },
            {
                'type': 'its_story',
                'defaults': {
                    'name': "Its Story",
                    'subtitle_tr': "1978'den bu güne",
                    'subtitle_en': "Since 1978",
                    'title_tr': "Kitti Hikayesi",
                    'title_en': "The Kitti Story",
                    'description_tr': "Minik kafalar için büyük bir hikaye yazıyoruz. Her ürünümüzde kalite, güvenlik ve sevgi var.",
                    'description_en': "We’re writing a big story for little heads — filled with quality, safety, and love.",
                },
                'image': 'section_5.png'
            },
            {
                'type': 'production_capacity',
                'defaults': {
                    'name': "Production Capacity",
                    'subtitle_tr': "Sipariş sürecini kolaylaştırıyoruz",
                    'subtitle_en': "Simplifying the Order Process",
                    'title_tr': "Üretim Kapasitemiz",
                    'title_en': "Our Production Capacity",
                    'description_tr': "Modern tesislerimizde günlük binlerce ürün üretiyoruz. Kaliteli hammaddeler ve uzman ekibimizle en iyisini sunuyoruz.",
                    'description_en': "We produce thousands of products daily in modern facilities with top-quality materials.",
                    'button_text_left_tr': "Detayları Gör",
                    'button_text_left_en': "See Details",
                    'button_url_left': "/contacts",
                    'button_text_right_tr': "Ürün Kataloğu",
                    'button_text_right_en': "Product Catalog",
                    'button_url_right': "/products",
                },
                'image': 'section_6.png'
            }
        ]

        for data in generic_sections_data:
            section_obj, created = GenericSection.objects.get_or_create(
                site=site,
                type=data['type'],
                defaults=data['defaults']
            )
            if created:
                if 'image' in data:
                    add_image_to_instance(section_obj, data['image'], field_name='image')
                if 'mobile_image' in data:
                    add_image_to_instance(section_obj, data['mobile_image'], field_name='mobile_image')
                self.stdout.write(self.style.SUCCESS(f"✅ Generic Section '{data['type']}' created."))

        # === 5️⃣ Hikayemiz Sayfası Bölümleri (GenericSectionOurStory) ===
        our_story_sections = [
            {
                'type': 'big_story',
                'defaults': {
                    'name': "Big Story Section",
                    'subtitle_tr': "Minik kafalar için", 'subtitle_en': "For little heads",
                    'title_tr': "BÜYÜK bir hikaye", 'title_en': "A BIG story",
                },
                'image': 'baby-contour.png'
            },
            {
                'type': 'all_over',
                'defaults': {
                    'name': "All Over Turkey Section",
                    'subtitle_tr': "TÜRKİYE'NİN", 'subtitle_en': "ALL OVER",
                    'title_tr': "DÖRT BİR YANINDA", 'title_en': "TURKEY",
                    'description_tr': "İstanbul'dan Iğdır'a kadar, nerede bir çocuk gülüşü varsa oradayız.",
                    'description_en': "From Istanbul to Iğdır, we are wherever there is a child's smile.",
                },
                'image': 'turkey-map-2.gif'
            },
            {
                'type': 'power_of_a_group',
                'defaults': {
                    'name': "Power of a Group Section",
                    'subtitle_tr': "1978", 'subtitle_en': "1978",
                    'title_tr': "Bir grubun gücüyle", 'title_en': "With the power of a group",
                    'description_tr': "Kitti, 1978'den beri tekstil sektöründe faaliyet gösteren ALK Group'un markalarından biridir.\n\nALK Group; Kitti gibi bir çok markasıyla hem Türkiye'de hem dünyada milyonlara ulaşır.",
                    'description_en': "Kitti is one of the brands of ALK Group, which has been operating in the textile industry since 1978.\n\nALK Group reaches millions in both Turkey and around the world with its many brands like Kitti.",
                },
                'subimage': 'alk-group.png',
                'image': 'Akal-Tekstil-2.png'
            },
            {
                'type': 'what_do_we_produce',
                'defaults': {
                    'name': "What We Produce Section",
                    'title_tr': "Neler Üretiyoruz?", 'title_en': "What Do We Produce?",
                    'description_tr': "Çocuklar için özel olarak tasarlanmış kaliteli ve güvenli aksesuarlar.",
                    'description_en': "Quality and safe accessories specially designed for children.",
                },
                'image': 'what-we-produce.png'
            },
            {
                'type': 'best_selling_accessories',
                'defaults': {
                    'name': "Best Selling Section",
                    'subtitle_tr': "Sizin için kolaylaştırıyoruz.", 'subtitle_en': "We make it easy for you.",
                    'title_tr': "En çok satan aksesuarlar", 'title_en': "Best-selling accessories",
                    'description_tr': "Kitti'nin en çok satan ürünleri, kalite ve güvenilirlik açısından müşterilerimizin tercihi olmuştur.\n\nYılların deneyimi ve sürekli gelişen tasarım anlayışımızla her yaştan kullanıcıya hitap ediyoruz.",
                    'description_en': "Kitti's best-selling products have been our customers' choice for quality and reliability.\n\nWith years of experience and our ever-evolving design approach, we appeal to users of all ages.",
                    'button_text_tr': "Ürünleri İncele", 'button_text_en': "Explore Products",
                    'button_url': "/products",
                },
                'image': 'kamyon-copy.png'
            },
            {
                'type': 'health_and_quality',
                'defaults': {
                    'name': "Health and Quality Section",
                    'subtitle_tr': "Önceliğimiz", 'subtitle_en': "Our Priority",
                    'title_tr': "Sağlık ve Kalite", 'title_en': "Health and Quality",
                    'description_tr': "Her ürünümüzde çocuk sağlığını ön planda tutuyoruz.\n\nZararsız materyaller ve güvenli üretim standartları ile ailelerin güvenini kazanıyoruz.",
                    'description_en': "In every product, we prioritize children's health.\n\nWe earn families' trust with harmless materials and safe production standards.",
                },
                'image': 'quality-image.png'
            },
            {
                'type': 'safe_facilities',
                'defaults': {
                    'name': "Safe Facilities Section",
                    'subtitle_tr': "Güvenli Tesisler", 'subtitle_en': "Safe Facilities",
                    'title_tr': "ve Korunaklı Üretim", 'title_en': "and Secure Production",
                    'description_tr': "Modern tesislerimizde güvenli üretim standartları uyguluyoruz.\n\nHer aşamada kalite kontrolü yaparak müşterilerimize en iyi ürünleri sunuyoruz.",
                    'description_en': "We apply safe production standards in our modern facilities.\n\nBy conducting quality control at every stage, we offer the best products to our customers.",
                    'button_text_tr': "Tesislerimizi Gezin", 'button_text_en': "Tour Our Facilities",
                    'button_url': "/factory",
                },
                'image': 'gunes-isik.png'
            },
            {
                'type': 'Harmless Materials', # Modeldeki 'choices' ile eşleşmeli
                'defaults': {
                    'name': "Harmless Materials Section",
                    'subtitle_tr': "Zararsız materyaller", 'subtitle_en': "Harmless Materials",
                    'title_tr': "Malzemeler ve Etiketler", 'title_en': "Materials and Labels",
                    'description_tr': "Tüm ürünlerimizde çocuk sağlığına uygun materyaller kullanıyoruz.\n\nEtiketlerimizde malzeme bilgileri ve güvenlik uyarıları yer almaktadır.",
                    'description_en': "We use materials suitable for children's health in all our products.\n\nOur labels include material information and safety warnings.",
                    'button_text_tr': "Malzeme Bilgileri", 'button_text_en': "Material Information",
                    'button_url': "/quality",
                },
                'image': 'kart-etiket.png'
            },
            {
                'type': 'growing_safely',
                'defaults': {
                    'name': "Growing Safely Section",
                    'title_tr': "Çocuklardan ilham, güvenle büyüme", 'title_en': "Inspired by children, growing safely",
                    'description_tr': "Her ürünümüzde çocuk güvenliği önceliğimizdir. Zararsız materyaller ve güvenli üretim standartları.",
                    'description_en': "Child safety is our priority in every product. Harmless materials and safe production standards.",
                },
                'image': 'smile-girl.png'
            },
            {
                'type': 'kitti_products',
                'defaults': {
                    'name': "Sell Kitti Products Section",
                    'title_tr': "Kitti ürünlerini satmak ister misiniz?", 'title_en': "Would you like to sell Kitti products?",
                    'button_text_tr': "Toptan Satış", 'button_text_en': "Wholesale",
                    'button_url': "/wholesale",
                },
                'subimage': 'logo.svg',
                'image': 'whole-sale.png'
            },
        ]

        for section_data in our_story_sections:
            section_obj, created = GenericSectionOurStory.objects.get_or_create(
                site=site,
                type=section_data['type'],
                defaults=section_data['defaults']
            )
            if created:
                if 'image' in section_data:
                    add_image_to_instance(section_obj, section_data['image'], field_name='image')
                if 'subimage' in section_data: # subimage için de kontrol
                    add_image_to_instance(section_obj, section_data['subimage'], field_name='subimage')
                self.stdout.write(self.style.SUCCESS(f"✅ Our Story Section '{section_data['type']}' created."))
        

        # === 7️⃣ İletişim Sayfası (Contact) ===
        self.stdout.write("Creating Contact Page sections...")
        contact_section, created = GenericSectionContact.objects.get_or_create(
            site=site,
            title_tr="Kitti ile iletişime geçin:",
            defaults={
                'title_en': "Get in touch with Kitti:",
                'description_tr': "Sorularınız için bizimle iletişime geçebilirsiniz. Size en kısa sürede dönüş yapacağız.",
                'description_en': "You can contact us with your questions. We will get back to you as soon as possible."
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS("✅ GenericSectionContact created."))

        # -- İletişim Adresleri --
        contact_addresses_data = [
            {
                'lookup': {'title_tr': "Merkez Adresimiz"},
                'defaults': {
                    'title_en': "Our Head Office",
                    'description_tr': "Merve Mah. Akabe Cad. No:16\nSancaktepe / İstanbul",
                    'description_en': "Merve Mah. Akabe Cad. No:16\nSancaktepe / Istanbul",
                    'tel': "444 10 47",
                    'tel_wp': "+90 532 703 09 90",
                }
            },
            {
                'lookup': {'title_tr': "Mağazamız"},
                'defaults': {
                    'title_en': "Our Store",
                    'description_tr': "Çakmakçılar Yokuşu No:24/1\nFatih / İstanbul",
                    'description_en': "Çakmakçılar Yokuşu No:24/1\nFatih / Istanbul",
                    'tel': "+90 212 520 90 60",
                    'tel_wp': "+90 532 703 09 90",
                }
            }
        ]
        for address_data in contact_addresses_data:
            address_obj, created = ContactAddresses.objects.get_or_create(
                contact=contact_section,
                **address_data['lookup'],
                defaults=address_data['defaults']
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Contact Address '{address_data['lookup']['title_tr']}' created."))

        # -- İletişim Mailleri --
        contact_mails_data = [
            "satis@kitti.com.tr",
            "info@alk.com.tr", # alk.com.tr'yi bir e-posta adresi olarak varsaydım
        ]
        for mail_address in contact_mails_data:
            mail_obj, created = ContactMails.objects.get_or_create(
                contact=contact_section,
                mail=mail_address
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Contact Mail '{mail_address}' created."))

        # === 8️⃣ Toptan Satış Sayfası (Wholesale) ===
        self.stdout.write("Creating Wholesale Page section...")
        wholesale_section, created = GenericSectionWholesale.objects.get_or_create(
            site=site,
            title_tr="Kobiler için Toptan Portal",
            defaults={
                'title_en': "Wholesale Portal for SMEs",
                'description_tr': "B2B toptan portal ile adeti düşük olan siparişlerinizi toptan portaldan verebilir, iş yerinize kargolatabilirsiniz.",
                'description_en': "With our B2B wholesale portal, you can place low-quantity orders and have them shipped to your workplace.",
                'info_text_tr': "*Portal, sadece kayıtlı iş ortaklarımızın kullanımına açıktır.",
                'info_text_en': "*The portal is only available to our registered business partners.",
                'button_top_title_tr': "Üye değil misiniz?",
                'button_top_title_en': "Not a member?",
                'button_top_text_tr': "Başvur",
                'button_top_text_en': "Apply",
                'button_top_url': "/contacts",
                'button_bottom_title_tr': "Üyeyseniz:",
                'button_bottom_title_en': "If you are a member:",
                'button_bottom_text_tr': "Giriş Yap",
                'button_bottom_text_en': "Log In",
                'button_bottom_url': "https://www.google.com",
            }
        )
        if created:
            add_image_to_instance(wholesale_section, "img-w-text-secondary-image.png")
            self.stdout.write(self.style.SUCCESS("✅ GenericSectionWholesale created."))


        # === 8️⃣ Footer Policies ===
        # Örnek HTML içeriği
        dummy_html_en = (
            "<h2>Placeholder Title</h2>"
            "<p><strong>Lorem Ipsum</strong> is simply dummy text of the printing and typesetting industry. "
            "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.</p>"
            "<p>It has survived not only five centuries, but also the leap into electronic typesetting, "
            "remaining essentially unchanged.</p>"
        )
        dummy_html_tr = (
            "<h2>Örnek Başlık</h2>"
            "<p><strong>Lorem Ipsum</strong>, dizgi ve baskı endüstrisinde kullanılan mıgır metinlerdir. "
            "Lorem Ipsum, adı bilinmeyen bir matbaacının bir hurufat numune kitabı oluşturmak üzere "
            "bir yazı galerisini alarak karıştırdığı 1500'lerden beri endüstri standardı sahte metinler "
            "olarak kullanılmıştır.</p>"
        )

        footer_policies = [
            {
                "lookup": {"title_tr": "Aydınlatma Metni"},
                "defaults": {
                    "title_en": "Information Text",
                    "description_tr": dummy_html_tr,
                    "description_en": dummy_html_en
                }
            },
            {
                "lookup": {"title_tr": "İleti Onay Metni"},
                "defaults": {
                    "title_en": "Message Consent Text",
                    "description_tr": dummy_html_tr,
                    "description_en": dummy_html_en
                }
            },
            {
                "lookup": {"title_tr": "Çerez Politikası"},
                "defaults": {
                    "title_en": "Cookie Policy",
                    "description_tr": dummy_html_tr,
                    "description_en": dummy_html_en
                }
            },
        ]

        for policy_data in footer_policies:
            policy_obj, created = FooterPolicy.objects.get_or_create(
                site=site,
                **policy_data['lookup'], # Sadece başlığa göre bul
                defaults=policy_data['defaults'] # Geri kalan veriyi defaults'a ata
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Footer Policy '{policy_data['lookup']['title_tr']}' created."))

        # === 9️⃣ Sosyal Medya ===
        SocialMedia.objects.get_or_create(site=site, icon="facebook", url="https://facebook.com")
        SocialMedia.objects.get_or_create(site=site, icon="instagram", url="https://instagram.com")

        # === 🔟 Footer Info ===
        self.stdout.write("Updating or creating Footer Info...")
        footer_info_obj, created = FooterInfo.objects.update_or_create(
            site=site, # Bu alana göre objeyi bul veya oluştur
            defaults={ # Bulunursa bu verilerle güncelle, bulunmazsa bu verilerle oluştur
                'footer_text_tr': 'kitti.com.tr © 2025 - Tüm hakları saklıdır.',
                'footer_text_en': 'kitti.com.tr © 2025 - All rights reserved.',
                'social_text_tr': 'Yenilikleri Kaçırmayın;',
                'social_text_en': "Don't miss the innovations;",
            }
        )

        # Logoyu sadece obje ilk kez oluşturuluyorsa ve logosu yoksa ekle
        if created and not footer_info_obj.logo:
            # Not: Bu dosyanın 'static/site_data/' klasöründe olduğundan emin olun.
            add_image_to_instance(footer_info_obj, "logo.svg", field_name='logo')
            self.stdout.write(self.style.SUCCESS("✅ FooterInfo created with logo."))
        elif created:
            self.stdout.write(self.style.SUCCESS("✅ FooterInfo created."))
        else:
            self.stdout.write("✅ FooterInfo updated with default texts.")

        self.stdout.write(self.style.SUCCESS("✅ Default multilingual site settings created successfully with images."))
