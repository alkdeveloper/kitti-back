from rest_framework import serializers
from .models import *

# --- Resim URL'si olmayan Serializer'lar (Değişiklik Yok) ---

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class FooterPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterPolicy
        fields = '__all__'

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'


# --- Resim URL'si Eklenmiş Serializer'lar ---

class HeaderSerializer(serializers.ModelSerializer):
    # 'image' alanı için tam URL döndürmek üzere SerializerMethodField kullanıyoruz.
    image = serializers.SerializerMethodField()

    class Meta:
        model = Header
        # 'image' alanı zaten yukarıda tanımlandığı için 'fields' içinde kalabilir.
        fields = ['id', 'title', 'description', 'image']

    def get_image(self, obj):
        """Header'daki 'image' alanı için tam URL oluşturur."""
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class GenericSectionSerializer(serializers.ModelSerializer):
    # 'image' alanı için tam URL döndürmek üzere SerializerMethodField kullanıyoruz.
    image = serializers.SerializerMethodField()

    class Meta:
        model = GenericSection
        # 'product' alanları Item modeline ait, onları da dahil edelim.
        fields = [
            'id', 'type', 'name', 'subtitle', 'title', 'description', 'image',
            'button_text_left', 'button_url_left', 'button_text_right', 'button_url_right',
            'product_1', 'product_2', 'product_3'
        ]

    def get_image(self, obj):
        """GenericSection'daki 'image' alanı için tam URL oluşturur."""
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class FooterInfoSerializer(serializers.ModelSerializer):
    # 'logo' alanı için tam URL döndürmek üzere SerializerMethodField kullanıyoruz.
    logo = serializers.SerializerMethodField()

    class Meta:
        model = FooterInfo
        fields = ['id', 'logo', 'footer_text']

    def get_logo(self, obj):
        """Footer'daki 'logo' alanı için tam URL oluşturur."""
        request = self.context.get('request')
        if obj.logo and hasattr(obj.logo, 'url'):
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None

# --- Ana, Kapsayıcı Serializer ---

class SiteSettingsSerializer(serializers.ModelSerializer):
    # 'logo' alanı için tam URL döndürmek üzere SerializerMethodField kullanıyoruz.
    logo = serializers.SerializerMethodField()
    
    # Nested serializer'lar, context'i otomatik olarak alacak ve
    # içlerindeki resim URL'leri de tam olarak oluşturulacaktır.
    menu_items = MenuItemSerializer(many=True, read_only=True)
    headers = HeaderSerializer(many=True, read_only=True)
    sections = GenericSectionSerializer(many=True, read_only=True)
    footer_policies = FooterPolicySerializer(many=True, read_only=True)
    social_links = SocialMediaSerializer(many=True, read_only=True)
    footer_info = FooterInfoSerializer(read_only=True)

    class Meta:
        model = SiteSettings
        # 'fields' listesine 'logo' alanını da ekliyoruz.
        fields = [
            'id', 'logo', 'site_title', 'site_description',
            'menu_items', 'headers', 'sections',
            'footer_policies', 'social_links', 'footer_info'
        ]

    def get_logo(self, obj):
        """Ana site ayarlarındaki 'logo' için tam URL oluşturur."""
        request = self.context.get('request')
        if obj.logo and hasattr(obj.logo, 'url'):
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None