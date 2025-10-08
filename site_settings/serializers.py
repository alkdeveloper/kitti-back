from rest_framework import serializers
from .models import *
from products.serializers import ProductSerializer

# --- DÜZELTİLMESİ GEREKEN SERIALIZER'LAR ---

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        # '__all__' yerine sadece frontend'in ihtiyaç duyduğu alanları belirtiyoruz.
        # 'modeltranslation' aktif dile göre 'text' alanını dolduracaktır.
        fields = ['id', 'href', 'text']

class FooterPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterPolicy
        # 'title' ve 'description' alanları çeviri içerdiği için alanları manuel belirtiyoruz.
        fields = ['id', 'title', 'description']

# --- Diğer Serializer'lar ---

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__' # Bu modelde çevrilmiş alan olmadığı için '__all__' kalabilir.

class HeaderSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Header
        # Bu zaten doğru yapılandırılmış.
        fields = ['id', 'title', 'description', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class GenericSectionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    product_1 = ProductSerializer(read_only=True)
    product_2 = ProductSerializer(read_only=True)
    product_3 = ProductSerializer(read_only=True)
    class Meta:
        model = GenericSection
        # Bu zaten doğru yapılandırılmış.
        fields = [
            'id', 'type', 'name', 'subtitle', 'title', 'description', 'image', 'mobile_image',
            'button_text_left', 'button_url_left', 'button_text_right', 'button_url_right',
            'product_1', 'product_2', 'product_3'
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class FooterInfoSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    class Meta:
        model = FooterInfo
        # 'footer_text' alanı çeviri içerdiği için alanları manuel belirtiyoruz.
        fields = ['id', 'logo', 'footer_text']

    def get_logo(self, obj):
        request = self.context.get('request')
        if obj.logo and hasattr(obj.logo, 'url'):
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None

# --- Ana, Kapsayıcı Serializer ---

class SiteSettingsSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    menu_items = MenuItemSerializer(many=True, read_only=True)
    headers = HeaderSerializer(many=True, read_only=True)
    sections = GenericSectionSerializer(many=True, read_only=True)
    footer_policies = FooterPolicySerializer(many=True, read_only=True)
    social_links = SocialMediaSerializer(many=True, read_only=True)
    footer_info = FooterInfoSerializer(read_only=True)

    class Meta:
        model = SiteSettings
        # 'site_title' ve 'site_description' çeviri içeriyor, bu zaten doğru yapılandırılmış.
        fields = [
            'id', 'logo', 'site_title', 'site_description',
            'menu_items', 'headers', 'sections',
            'footer_policies', 'social_links', 'footer_info'
        ]

    def get_logo(self, obj):
        request = self.context.get('request')
        if obj.logo and hasattr(obj.logo, 'url'):
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None