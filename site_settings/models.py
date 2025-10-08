from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from products.models import Item  # 3 ürün seçmek için kullanılacak

class SiteSettings(models.Model):
    logo = models.FileField(upload_to='site/logo/', blank=True, null=True)
    site_title = models.CharField(max_length=255)
    site_description = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.site_title


class MenuItem(models.Model):
    site = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='menu_items')
    href = models.CharField(max_length=255)
    text = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.text


class Header(models.Model):
    site = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='headers')
    title = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    image = models.FileField(upload_to='site/header/', blank=True, null=True)

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
    button_url_left = models.CharField(blank=True, null=True)
    button_text_right = models.CharField(max_length=255, blank=True, null=True)
    button_url_right = models.CharField(blank=True, null=True)

    # Favoriler için
    product_1 = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    product_2 = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    product_3 = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    def __str__(self):
        return f"{self.get_type_display()} - {self.name}"


class FooterPolicy(models.Model):
    site = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='footer_policies')
    title = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.title


class SocialMedia(models.Model):
    site = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='social_links')
    icon = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.icon


class FooterInfo(models.Model):
    site = models.OneToOneField(SiteSettings, on_delete=models.CASCADE, related_name='footer_info')
    logo = models.FileField(upload_to='site/footer/', blank=True, null=True)
    footer_text = models.CharField(max_length=255, default='kitti.com.tr © 2025 - Tüm hakları saklıdır.')

    def __str__(self):
        return "Footer Info"