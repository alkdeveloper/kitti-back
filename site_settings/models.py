from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from products.models import Item  # 3 ürün seçmek için kullanılacak

class SiteSettings(models.Model):
    logo = models.FileField(upload_to='site/logo/', blank=True, null=True)
    favicon = models.FileField(
        upload_to='site/favicon/', 
        blank=True, 
        null=True, 
        help_text="Site ikonu (favicon). Genellikle .ico, .png veya .svg formatında olur."
    )
    site_title = models.CharField(max_length=255)
    site_description = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = "Genel Site Ayarı"
        verbose_name_plural = "Genel Site Ayarları"

    def __str__(self):
        return self.site_title


class MenuItem(models.Model):
    site = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='menu_items')
    href = models.CharField(max_length=255)
    text = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']
        verbose_name = "Menü Elemanı"
        verbose_name_plural = "Menü Elemanları"

    def __str__(self):
        return self.text


class Header(models.Model):
    site = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='headers')
    title = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    image = models.FileField(upload_to='site/header/', blank=True, null=True)

    class Meta:
        verbose_name = "Ana Sayfa Header"
        verbose_name_plural = "Ana Sayfa Header Ayarları"

    def __str__(self):
        return f"Header: {self.title}"

class GenericSection(models.Model):
    SECTION_TYPES = [
        ('whats_kitty', "What's Kitty"),
        ('favorites_of_season', 'Favorites of Season'),
        ('who_are_we', 'Who Are We'),
        ('from_the_workshop', 'From the Workshop'),
        ('its_story', "Its Story"),
        ('production_capacity', 'Production Capacity'),
        ('generic', 'Generic Section'),
    ]

    site = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='sections')
    type = models.CharField(max_length=50, choices=SECTION_TYPES, default='generic')
    
    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)

    mobile_image = models.FileField(upload_to='site/sections/', blank=True, null=True)
    image = models.FileField(upload_to='site/sections/', blank=True, null=True)
    
    # Butonlar
    button_text_left = models.CharField(max_length=255, blank=True, null=True)
    button_url_left = models.CharField(max_length=500, blank=True, null=True)
    button_text_right = models.CharField(max_length=255, blank=True, null=True)
    button_url_right = models.CharField(max_length=500, blank=True, null=True)

    # Favoriler için
    product_1 = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    product_2 = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    product_3 = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    class Meta:
        verbose_name = "Ana Sayfa Bölümü"
        verbose_name_plural = "Ana Sayfa Bölüm Ayarları"

    def __str__(self):
        return f"{self.get_type_display()} - {self.name}"

class GenericSectionOurStory(models.Model):
    SECTION_TYPES = [
        ('big_story', "Big Story"),
        ('all_over', 'All Over'),
        ('power_of_a_group', 'Power Of a Group'),
        ('what_do_we_produce', 'What Do We Produce'),
        ('best_selling_accessories', "Best Selling Accessories"),
        ('health_and_quality', 'Health and Quality'),
        ('safe_facilities', 'Safe Facilities'),
        ('harmless_materials', 'Harmless Materials'),
        ('growing_safely', 'Growing Safely'),
        ('kitti_products', 'Kitti Products'),
    ]

    site = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='sections_our_story')
    type = models.CharField(max_length=50, choices=SECTION_TYPES, default='generic_our_story')
    
    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)

    subimage = models.FileField(upload_to='site/sections/our_story', blank=True, null=True)
    mobile_image = models.FileField(upload_to='site/sections/our_story', blank=True, null=True)
    image = models.FileField(upload_to='site/sections/our_story', blank=True, null=True)
    
    # Butonlar
    button_text = models.CharField(max_length=255, blank=True, null=True)
    button_url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = "Hikayemiz Sayfası Bölümü"
        verbose_name_plural = "Hikayemiz Sayfası Bölümleri"

    def __str__(self):
        return f"{self.get_type_display()} - {self.name}"

class GenericSectionContact(models.Model):
    site = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='sections_contact')

    title = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = "İletişim Sayfası Ayarı"
        verbose_name_plural = "İletişim Sayfası Ayarları"

    def __str__(self):
        return f"{self.title}"

class ContactAddresses(models.Model):
    contact = models.ForeignKey(GenericSectionContact, on_delete=models.CASCADE, related_name='sections_address')

    title = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)

    tel = models.CharField(max_length=255)
    tel_wp = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title}"
    
class ContactMails(models.Model):
    contact = models.ForeignKey(GenericSectionContact, on_delete=models.CASCADE, related_name='sections_mails')

    mail = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.mail}"

class GenericSectionWholesale(models.Model):
    site = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='sections_wholasale')

    title = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    info_text = RichTextField(blank=True, null=True)

    image = models.FileField(upload_to='site/sections/wholasale', blank=True, null=True)
    
    # Butonlar
    button_top_title = models.CharField(max_length=255, blank=True, null=True)
    button_top_text = models.CharField(max_length=255, blank=True, null=True)
    button_top_url = models.CharField(max_length=500, blank=True, null=True)
    button_bottom_title = models.CharField(max_length=255, blank=True, null=True)
    button_bottom_text = models.CharField(max_length=255, blank=True, null=True)
    button_bottom_url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = "Toptan Satış Sayfası Ayarı"
        verbose_name_plural = "Toptan Satış Sayfası Ayarları"

    def __str__(self):
        return f"{self.title}"

class FooterPolicy(models.Model):
    site = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='footer_policies')
    title = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = "Politika"
        verbose_name_plural = "Politika Ayarları"

    def __str__(self):
        return self.title


class SocialMedia(models.Model):
    site = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='social_links')
    icon = models.CharField(max_length=50)
    url = models.CharField(max_length=500)  # URLField yerine CharField - "#" gibi değerler için

    class Meta:
        verbose_name = "Sosyal Medya Linki"
        verbose_name_plural = "Sosyal Medya Linkleri"

    def __str__(self):
        return self.icon


class FooterInfo(models.Model):
    site = models.OneToOneField(SiteSettings, on_delete=models.CASCADE, related_name='footer_info')
    logo = models.FileField(upload_to='site/footer/', blank=True, null=True)
    footer_text = models.CharField(max_length=255, default='kitti.com.tr © 2025 - Tüm hakları saklıdır.')
    social_text = models.CharField(max_length=255, default='Yenilikleri Kaçırmayın;')

    class Meta:
        verbose_name = "Footer Bilgisi"
        verbose_name_plural = "Footer Bilgi Ayarları"

    def __str__(self):
        return "Footer Info"


class FAQItem(models.Model):
    """Sıkça Sorulan Sorular (FAQ) Modeli"""
    site = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='faq_items')
    question = models.CharField(max_length=500)
    answer = RichTextField()
    order = models.IntegerField(default=0, help_text="Sıralama için kullanılır")

    class Meta:
        verbose_name = "FAQ Öğesi"
        verbose_name_plural = "FAQ Öğeleri"
        ordering = ['order', 'id']

    def __str__(self):
        return self.question

