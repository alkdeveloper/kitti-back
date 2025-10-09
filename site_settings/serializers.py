from rest_framework import serializers
from .models import *
from products.serializers import ProductSerializer
from django.utils.translation import get_language

# -----------------------------------------------------------------------------
# YARDIMCI SERIALIZER'LAR (BAŞKA YERDE KULLANILACAK)
# -----------------------------------------------------------------------------

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'href', 'text']

class HeaderSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Header
        fields = ['id', 'title', 'description', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

class GenericSectionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    mobile_image = serializers.SerializerMethodField()
    product_1 = ProductSerializer(read_only=True)
    product_2 = ProductSerializer(read_only=True)
    product_3 = ProductSerializer(read_only=True)

    class Meta:
        model = GenericSection
        fields = [
            'id', 'type', 'name', 'subtitle', 'title', 'description', 'image', 'mobile_image',
            'button_text_left', 'button_url_left', 'button_text_right', 'button_url_right',
            'product_1', 'product_2', 'product_3'
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def get_mobile_image(self, obj):
        request = self.context.get('request')
        if obj.mobile_image and hasattr(obj.mobile_image, 'url'):
            return request.build_absolute_uri(obj.mobile_image.url) if request else obj.mobile_image.url
        return None

# --- YENİ EKLENEN MODELLER İÇİN SERIALIZER'LAR ---

class GenericSectionOurStorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subimage = serializers.SerializerMethodField()
    mobile_image = serializers.SerializerMethodField()
    
    class Meta:
        model = GenericSectionOurStory
        # '__all__' yerine, frontend'in ihtiyaç duyduğu alanları manuel olarak listeliyoruz.
        fields = [
            'id', 
            'type', 
            'name', 
            'subtitle', 
            'title',
            'description', 
            'subimage', 
            'mobile_image', 
            'image',
            'button_text', 
            'button_url'
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def get_subimage(self, obj):
        request = self.context.get('request')
        if obj.subimage and hasattr(obj.subimage, 'url'):
            return request.build_absolute_uri(obj.subimage.url) if request else obj.subimage.url
        return None
        
    def get_mobile_image(self, obj):
        request = self.context.get('request')
        if obj.mobile_image and hasattr(obj.mobile_image, 'url'):
            return request.build_absolute_uri(obj.mobile_image.url) if request else obj.mobile_image.url
        return None

class ContactAddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactAddresses
        fields = [
            'id', 
            'title', 
            'description', 
            'tel',
            'tel_wp',
        ]

class ContactMailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMails
        fields = [
            'id', 
            'mail',
        ]

class GenericSectionContactSerializer(serializers.ModelSerializer):
    # İlişkili adresleri ve mailleri burada iç içe gösteriyoruz
    sections_address = ContactAddressesSerializer(many=True, read_only=True)
    sections_mails = ContactMailsSerializer(many=True, read_only=True)

    class Meta:
        model = GenericSectionContact
        fields = ['id', 'title', 'description', 'sections_address', 'sections_mails']


class GenericSectionWholesaleSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = GenericSectionWholesale
        # '__all__' yerine, modeldeki tüm ilgili alanları manuel olarak listeliyoruz.
        fields = [
            'id', 
            'title', 
            'description', 
            'info_text', 
            'image',
            'button_top_title', 
            'button_top_text', 
            'button_top_url',
            'button_bottom_title', 
            'button_bottom_text', 
            'button_bottom_url'
        ]
    
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

class FooterPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterPolicy
        fields = ['id', 'title', 'description']

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['id', 'icon', 'url']

class FooterInfoSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    # DÜZELTME: Çevrilecek alanları SerializerMethodField olarak tanımlıyoruz.
    footer_text = serializers.SerializerMethodField()
    social_text = serializers.SerializerMethodField()

    class Meta:
        model = FooterInfo
        # Alanlar yukarıda tanımlandığı için bu liste doğru.
        fields = ['id', 'logo', 'footer_text', 'social_text']

    def get_logo(self, obj):
        request = self.context.get('request')
        if obj.logo and hasattr(obj.logo, 'url'):
            return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url
        return None

    # YENİ EKLENDİ: Aktif dile göre footer_text'i getiren metod.
    def get_footer_text(self, obj):
        lang = get_language() # View'da activate() ile ayarlanan aktif dili alır.
        if lang == 'en' and hasattr(obj, 'footer_text_en'):
            return obj.footer_text_en or obj.footer_text_tr # İngilizce yoksa Türkçe'ye fallback
        return obj.footer_text_tr or obj.footer_text_en

    # YENİ EKLENDİ: Aktif dile göre social_text'i getiren metod.
    def get_social_text(self, obj):
        lang = get_language()
        if lang == 'en' and hasattr(obj, 'social_text_en'):
            return obj.social_text_en or obj.social_text_tr
        return obj.social_text_tr or obj.social_text_en

# -----------------------------------------------------------------------------
# ANA KAPSAYICI SERIALIZER (SITE SETTINGS)
# -----------------------------------------------------------------------------

class SiteSettingsSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    
    # Mevcut ilişkiler
    menu_items = MenuItemSerializer(many=True, read_only=True)
    headers = HeaderSerializer(many=True, read_only=True)
    sections = GenericSectionSerializer(many=True, read_only=True)
    footer_policies = FooterPolicySerializer(many=True, read_only=True)
    social_links = SocialMediaSerializer(many=True, read_only=True)
    footer_info = FooterInfoSerializer(read_only=True)
    
    # YENİ EKLENEN İLİŞKİLER
    sections_our_story = GenericSectionOurStorySerializer(many=True, read_only=True)
    sections_contact = GenericSectionContactSerializer(many=True, read_only=True) # Genellikle 1 tane olacak
    sections_wholasale = GenericSectionWholesaleSerializer(many=True, read_only=True) # Genellikle 1 tane olacak

    class Meta:
        model = SiteSettings
        fields = [
            'id', 'logo', 'favicon', 'site_title', 'site_description',
            'menu_items', 'headers', 'sections',
            'footer_policies', 'social_links', 'footer_info',
            # Yeni alanları da ana serializer'a ekliyoruz
            'sections_our_story', 'sections_contact', 'sections_wholasale',
        ]

    def get_logo(self, obj):
        request = self.context.get('request')
        if obj.logo and hasattr(obj.logo, 'url'):
            return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url
        return None