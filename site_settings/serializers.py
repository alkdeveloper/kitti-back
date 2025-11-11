from rest_framework import serializers
from .models import *
from products.serializers import ProductSerializer
from django.utils.translation import get_language

# -----------------------------------------------------------------------------
# YARDIMCI SERIALIZER'LAR (BAŞKA YERDE KULLANILACAK)
# -----------------------------------------------------------------------------

class MenuItemSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    
    class Meta:
        model = MenuItem
        fields = ['id', 'href', 'text', 'text_tr', 'text_en']
        extra_kwargs = {
            'text_tr': {'required': False},
            'text_en': {'required': False},
        }

    def get_text(self, obj):
        lang = get_language()
        if lang == 'en' and hasattr(obj, 'text_en'):
            return obj.text_en or obj.text_tr
        return obj.text_tr or obj.text_en
    
    def to_internal_value(self, data):
        # Request'ten lang parametresini al
        request = self.context.get('request')
        lang = 'tr'  # Varsayılan
        if request:
            lang = request.query_params.get('lang', 'tr')
        
        # text'i lang'a göre map et ve orijinal alanı kaldır
        if isinstance(data, dict):
            data = data.copy()
            if 'text' in data:
                if lang == 'en' and 'text_en' not in data:
                    data['text_en'] = data['text']
                    data.pop('text', None)
                elif lang == 'tr' and 'text_tr' not in data:
                    data['text_tr'] = data['text']
                    data.pop('text', None)
        return super().to_internal_value(data)

class HeaderSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Header
        fields = [
            'id', 
            'title', 
            'title_tr',
            'title_en',
            'description', 
            'description_tr',
            'description_en',
            'image', 
            'image_url'
        ]
        extra_kwargs = {
            'image': {'write_only': True, 'required': False, 'allow_null': True},
            'title_tr': {'required': False},
            'title_en': {'required': False},
            'description_tr': {'required': False},
            'description_en': {'required': False},
        }
    
    def to_internal_value(self, data):
        # Request'ten lang parametresini al
        request = self.context.get('request')
        lang = 'tr'  # Varsayılan
        if request:
            lang = request.query_params.get('lang', 'tr')
        
        # Boş string'leri None'a çevir ve lang'a göre map et
        if isinstance(data, dict):
            data = data.copy()
            if 'image' in data and data['image'] == '':
                data['image'] = None
            
            # title ve description'i lang'a göre map et
            if 'title' in data:
                if lang == 'en' and 'title_en' not in data:
                    data['title_en'] = data['title']
                    data.pop('title', None)
                elif lang == 'tr' and 'title_tr' not in data:
                    data['title_tr'] = data['title']
                    data.pop('title', None)
            
            if 'description' in data:
                if lang == 'en' and 'description_en' not in data:
                    data['description_en'] = data['description']
                    data.pop('description', None)
                elif lang == 'tr' and 'description_tr' not in data:
                    data['description_tr'] = data['description']
                    data.pop('description', None)
        
        return super().to_internal_value(data)

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

class GenericSectionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    mobile_image_url = serializers.SerializerMethodField()
    product_1 = ProductSerializer(read_only=True)
    product_2 = ProductSerializer(read_only=True)
    product_3 = ProductSerializer(read_only=True)

    class Meta:
        model = GenericSection
        fields = [
            'id', 'type', 
            'name', 'name_tr', 'name_en',
            'subtitle', 'subtitle_tr', 'subtitle_en',
            'title', 'title_tr', 'title_en',
            'description', 'description_tr', 'description_en',
            'image', 'image_url', 'mobile_image', 'mobile_image_url',
            'button_text_left', 'button_text_left_tr', 'button_text_left_en',
            'button_url_left', 
            'button_text_right', 'button_text_right_tr', 'button_text_right_en',
            'button_url_right',
            'product_1', 'product_2', 'product_3'
        ]
        extra_kwargs = {
            'image': {'write_only': True, 'required': False, 'allow_null': True},
            'mobile_image': {'write_only': True, 'required': False, 'allow_null': True},
            'product_1': {'write_only': False, 'required': False, 'allow_null': True},
            'product_2': {'write_only': False, 'required': False, 'allow_null': True},
            'product_3': {'write_only': False, 'required': False, 'allow_null': True},
            'name_tr': {'required': False},
            'name_en': {'required': False},
            'subtitle_tr': {'required': False},
            'subtitle_en': {'required': False},
            'title_tr': {'required': False},
            'title_en': {'required': False},
            'description_tr': {'required': False},
            'description_en': {'required': False},
            'button_text_left_tr': {'required': False},
            'button_text_left_en': {'required': False},
            'button_text_right_tr': {'required': False},
            'button_text_right_en': {'required': False},
        }
    
    def to_internal_value(self, data):
        # Request'ten lang parametresini al
        request = self.context.get('request')
        lang = 'tr'  # Varsayılan
        if request:
            lang = request.query_params.get('lang', 'tr')
        
        # Boş string'leri None'a çevir ve lang'a göre map et
        if isinstance(data, dict):
            data = data.copy()
            if 'image' in data and data['image'] == '':
                data['image'] = None
            if 'mobile_image' in data and data['mobile_image'] == '':
                data['mobile_image'] = None
            
            # name, subtitle, title, description, button_text_left, button_text_right'i lang'a göre map et
            for field in ['name', 'subtitle', 'title', 'description', 'button_text_left', 'button_text_right']:
                if field in data:
                    if lang == 'en' and f'{field}_en' not in data:
                        data[f'{field}_en'] = data[field]
                        data.pop(field, None)
                    elif lang == 'tr' and f'{field}_tr' not in data:
                        data[f'{field}_tr'] = data[field]
                        data.pop(field, None)
            
            # product_1, product_2, product_3'ü ID'ye çevir
            for product_field in ['product_1', 'product_2', 'product_3']:
                if product_field in data:
                    if isinstance(data[product_field], dict):
                        data[product_field] = data[product_field].get('id')
        
        return super().to_internal_value(data)

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def get_mobile_image_url(self, obj):
        request = self.context.get('request')
        if obj.mobile_image and hasattr(obj.mobile_image, 'url'):
            return request.build_absolute_uri(obj.mobile_image.url) if request else obj.mobile_image.url
        return None

# --- YENİ EKLENEN MODELLER İÇİN SERIALIZER'LAR ---

class GenericSectionOurStorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    subimage_url = serializers.SerializerMethodField()
    mobile_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = GenericSectionOurStory
        fields = [
            'id', 'type', 'name', 
            'subtitle', 'subtitle_tr', 'subtitle_en',
            'title', 'title_tr', 'title_en', 
            'description', 'description_tr', 'description_en',
            'subimage', 'subimage_url', 'mobile_image', 'mobile_image_url', 
            'image', 'image_url', 
            'button_text', 'button_text_tr', 'button_text_en',
            'button_url'
        ]
        extra_kwargs = {
            'image': {'write_only': True, 'required': False, 'allow_null': True},
            'subimage': {'write_only': True, 'required': False, 'allow_null': True},
            'mobile_image': {'write_only': True, 'required': False, 'allow_null': True},
            'subtitle_tr': {'required': False},
            'subtitle_en': {'required': False},
            'title_tr': {'required': False},
            'title_en': {'required': False},
            'description_tr': {'required': False},
            'description_en': {'required': False},
            'button_text_tr': {'required': False},
            'button_text_en': {'required': False},
        }
    
    def to_internal_value(self, data):
        # Request'ten lang parametresini al
        request = self.context.get('request')
        lang = 'tr'  # Varsayılan
        if request:
            lang = request.query_params.get('lang', 'tr')
        
        # Boş string'leri None'a çevir ve lang'a göre map et
        if isinstance(data, dict):
            data = data.copy()
            # Dosya alanları için boş string'leri None'a çevir
            for field in ['image', 'subimage', 'mobile_image']:
                if field in data and data[field] == '':
                    data[field] = None
            
            # Çoklu dil alanlarını lang'a göre map et
            for field in ['subtitle', 'title', 'description', 'button_text']:
                if field in data:
                    if lang == 'en' and f'{field}_en' not in data:
                        data[f'{field}_en'] = data[field]
                        data.pop(field, None)
                    elif lang == 'tr' and f'{field}_tr' not in data:
                        data[f'{field}_tr'] = data[field]
                        data.pop(field, None)
        
        return super().to_internal_value(data)

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def get_subimage_url(self, obj):
        request = self.context.get('request')
        if obj.subimage and hasattr(obj.subimage, 'url'):
            return request.build_absolute_uri(obj.subimage.url) if request else obj.subimage.url
        return None
        
    def get_mobile_image_url(self, obj):
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
            'title_tr',
            'title_en',
            'description', 
            'description_tr',
            'description_en',
            'tel',
            'tel_wp',
        ]
        extra_kwargs = {
            'title_tr': {'required': False},
            'title_en': {'required': False},
            'description_tr': {'required': False},
            'description_en': {'required': False},
        }
    
    def to_internal_value(self, data):
        # Request'ten lang parametresini al
        request = self.context.get('request')
        lang = 'tr'  # Varsayılan
        if request:
            lang = request.query_params.get('lang', 'tr')
        
        # title ve description'i lang'a göre map et ve orijinal alanları kaldır
        if isinstance(data, dict):
            data = data.copy()
            if 'title' in data:
                if lang == 'en' and 'title_en' not in data:
                    data['title_en'] = data['title']
                    # title alanını kaldır (sadece title_en kullanılacak)
                    data.pop('title', None)
                elif lang == 'tr' and 'title_tr' not in data:
                    data['title_tr'] = data['title']
                    # title alanını kaldır (sadece title_tr kullanılacak)
                    data.pop('title', None)
            if 'description' in data:
                if lang == 'en' and 'description_en' not in data:
                    data['description_en'] = data['description']
                    # description alanını kaldır (sadece description_en kullanılacak)
                    data.pop('description', None)
                elif lang == 'tr' and 'description_tr' not in data:
                    data['description_tr'] = data['description']
                    # description alanını kaldır (sadece description_tr kullanılacak)
                    data.pop('description', None)
        return super().to_internal_value(data)

class ContactMailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMails
        fields = [
            'id', 
            'mail',
        ]

class GenericSectionContactSerializer(serializers.ModelSerializer):
    # İlişkili adresleri ve mailleri burada iç içe gösteriyoruz
    sections_address = ContactAddressesSerializer(many=True, required=False)
    sections_mails = ContactMailsSerializer(many=True, required=False)

    class Meta:
        model = GenericSectionContact
        fields = [
            'id', 
            'title', 
            'title_tr',
            'title_en',
            'description', 
            'description_tr',
            'description_en',
            'sections_address', 
            'sections_mails'
        ]
        extra_kwargs = {
            'title_tr': {'required': False},
            'title_en': {'required': False},
            'description_tr': {'required': False},
            'description_en': {'required': False},
        }
    
    def to_internal_value(self, data):
        # Request'ten lang parametresini al
        request = self.context.get('request')
        lang = 'tr'  # Varsayılan
        if request:
            lang = request.query_params.get('lang', 'tr')
        
        # title ve description'i lang'a göre map et ve orijinal alanları kaldır
        if isinstance(data, dict):
            data = data.copy()
            if 'title' in data:
                if lang == 'en' and 'title_en' not in data:
                    data['title_en'] = data['title']
                    # title alanını kaldır (sadece title_en kullanılacak)
                    data.pop('title', None)
                elif lang == 'tr' and 'title_tr' not in data:
                    data['title_tr'] = data['title']
                    # title alanını kaldır (sadece title_tr kullanılacak)
                    data.pop('title', None)
            if 'description' in data:
                if lang == 'en' and 'description_en' not in data:
                    data['description_en'] = data['description']
                    # description alanını kaldır (sadece description_en kullanılacak)
                    data.pop('description', None)
                elif lang == 'tr' and 'description_tr' not in data:
                    data['description_tr'] = data['description']
                    # description alanını kaldır (sadece description_tr kullanılacak)
                    data.pop('description', None)
        return super().to_internal_value(data)


class GenericSectionWholesaleSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = GenericSectionWholesale
        fields = [
            'id', 'title', 'title_tr', 'title_en',
            'description', 'description_tr', 'description_en',
            'info_text', 'info_text_tr', 'info_text_en',
            'image', 'image_url',
            'button_top_title', 'button_top_title_tr', 'button_top_title_en',
            'button_top_text', 'button_top_text_tr', 'button_top_text_en',
            'button_top_url',
            'button_bottom_title', 'button_bottom_title_tr', 'button_bottom_title_en',
            'button_bottom_text', 'button_bottom_text_tr', 'button_bottom_text_en',
            'button_bottom_url'
        ]
        extra_kwargs = {
            'image': {'write_only': True, 'required': False, 'allow_null': True},
            'title_tr': {'required': False},
            'title_en': {'required': False},
            'description_tr': {'required': False},
            'description_en': {'required': False},
            'info_text_tr': {'required': False},
            'info_text_en': {'required': False},
            'button_top_title_tr': {'required': False},
            'button_top_title_en': {'required': False},
            'button_top_text_tr': {'required': False},
            'button_top_text_en': {'required': False},
            'button_bottom_title_tr': {'required': False},
            'button_bottom_title_en': {'required': False},
            'button_bottom_text_tr': {'required': False},
            'button_bottom_text_en': {'required': False},
        }
    
    def to_internal_value(self, data):
        # Request'ten lang parametresini al
        request = self.context.get('request')
        lang = 'tr'  # Varsayılan
        if request:
            lang = request.query_params.get('lang', 'tr')
        
        # Boş string'leri None'a çevir
        if isinstance(data, dict):
            data = data.copy()
            if 'image' in data and data['image'] == '':
                data['image'] = None
            
            # title, description, info_text ve buton alanlarını lang'a göre map et
            for field in ['title', 'description', 'info_text', 'button_top_title', 'button_top_text', 'button_bottom_title', 'button_bottom_text']:
                if field in data:
                    if lang == 'en' and f'{field}_en' not in data:
                        data[f'{field}_en'] = data[field]
                        data.pop(field, None)
                    elif lang == 'tr' and f'{field}_tr' not in data:
                        data[f'{field}_tr'] = data[field]
                        data.pop(field, None)
        
        return super().to_internal_value(data)
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

class FooterPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterPolicy
        fields = [
            'id', 
            'title', 
            'title_tr',
            'title_en',
            'description', 
            'description_tr',
            'description_en'
        ]
        extra_kwargs = {
            'title_tr': {'required': False},
            'title_en': {'required': False},
            'description_tr': {'required': False},
            'description_en': {'required': False},
        }
    
    def to_internal_value(self, data):
        # Request'ten lang parametresini al
        request = self.context.get('request')
        lang = 'tr'  # Varsayılan
        if request:
            lang = request.query_params.get('lang', 'tr')
        
        # title ve description'i lang'a göre map et ve orijinal alanları kaldır
        if isinstance(data, dict):
            data = data.copy()
            if 'title' in data:
                if lang == 'en' and 'title_en' not in data:
                    data['title_en'] = data['title']
                    data.pop('title', None)
                elif lang == 'tr' and 'title_tr' not in data:
                    data['title_tr'] = data['title']
                    data.pop('title', None)
            if 'description' in data:
                if lang == 'en' and 'description_en' not in data:
                    data['description_en'] = data['description']
                    data.pop('description', None)
                elif lang == 'tr' and 'description_tr' not in data:
                    data['description_tr'] = data['description']
                    data.pop('description', None)
        return super().to_internal_value(data)

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['id', 'icon', 'url']
        extra_kwargs = {
            'url': {'required': False, 'allow_blank': True},
        }
    
    def validate_url(self, value):
        # Boş string veya "#" için geçerli bir placeholder URL döndür
        if not value or value == "" or value == "#":
            return "http://localhost/#"
        # Eğer "#" ile başlıyorsa, geçerli bir URL formatına çevir
        if value.startswith("#"):
            return "http://localhost" + value
        return value

class FAQItemSerializer(serializers.ModelSerializer):
    """FAQ Öğesi Serializer"""
    question = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()
    
    class Meta:
        model = FAQItem
        fields = [
            'id', 
            'question', 'question_tr', 'question_en',
            'answer', 'answer_tr', 'answer_en',
            'order'
        ]
        extra_kwargs = {
            'question_tr': {'required': False},
            'question_en': {'required': False},
            'answer_tr': {'required': False},
            'answer_en': {'required': False},
            'order': {'required': False},
        }
    
    def get_question(self, obj):
        """Aktif dile göre question döndür"""
        language = get_language()
        if language == 'en':
            return obj.question_en or obj.question_tr
        return obj.question_tr or obj.question_en
    
    def get_answer(self, obj):
        """Aktif dile göre answer döndür"""
        language = get_language()
        if language == 'en':
            return obj.answer_en or obj.answer_tr
        return obj.answer_tr or obj.answer_en
    
    def to_internal_value(self, data):
        # Request'ten lang parametresini al
        request = self.context.get('request')
        lang = 'tr'  # Varsayılan
        if request:
            lang = request.query_params.get('lang', 'tr')
        
        # Boş string'leri None'a çevir ve lang'a göre map et
        if isinstance(data, dict):
            data = data.copy()
            
            # question ve answer'i lang'a göre map et
            for field in ['question', 'answer']:
                if field in data:
                    if lang == 'en' and f'{field}_en' not in data:
                        data[f'{field}_en'] = data[field]
                        data.pop(field, None)
                    elif lang == 'tr' and f'{field}_tr' not in data:
                        data[f'{field}_tr'] = data[field]
                        data.pop(field, None)
        
        return super().to_internal_value(data)

class PageMetaSerializer(serializers.ModelSerializer):
    """Sayfa Meta Bilgileri Serializer"""
    meta_title = serializers.SerializerMethodField()
    meta_description = serializers.SerializerMethodField()
    
    class Meta:
        model = PageMeta
        fields = [
            'id', 'page',
            'meta_title', 'meta_title_tr', 'meta_title_en',
            'meta_description', 'meta_description_tr', 'meta_description_en'
        ]
        extra_kwargs = {
            'meta_title_tr': {'required': False},
            'meta_title_en': {'required': False},
            'meta_description_tr': {'required': False},
            'meta_description_en': {'required': False},
        }
    
    def get_meta_title(self, obj):
        """Aktif dile göre meta_title döndür"""
        language = get_language()
        if language == 'en':
            return obj.meta_title_en or obj.meta_title_tr
        return obj.meta_title_tr or obj.meta_title_en
    
    def get_meta_description(self, obj):
        """Aktif dile göre meta_description döndür"""
        language = get_language()
        if language == 'en':
            return obj.meta_description_en or obj.meta_description_tr
        return obj.meta_description_tr or obj.meta_description_en
    
    def to_internal_value(self, data):
        # Request'ten lang parametresini al
        request = self.context.get('request')
        lang = 'tr'  # Varsayılan
        if request:
            lang = request.query_params.get('lang', 'tr')
        
        # Boş string'leri None'a çevir ve lang'a göre map et
        if isinstance(data, dict):
            data = data.copy()
            
            # meta_title ve meta_description'i lang'a göre map et
            for field in ['meta_title', 'meta_description']:
                if field in data:
                    if lang == 'en' and f'{field}_en' not in data:
                        data[f'{field}_en'] = data[field]
                        data.pop(field, None)
                    elif lang == 'tr' and f'{field}_tr' not in data:
                        data[f'{field}_tr'] = data[field]
                        data.pop(field, None)
        
        return super().to_internal_value(data)

class FooterInfoSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    footer_text = serializers.SerializerMethodField()
    social_text = serializers.SerializerMethodField()

    class Meta:
        model = FooterInfo
        fields = [
            'id', 
            'logo', 
            'logo_url', 
            'footer_text', 
            'footer_text_tr',
            'footer_text_en',
            'social_text',
            'social_text_tr',
            'social_text_en'
        ]
        extra_kwargs = {
            'logo': {'write_only': True, 'required': False, 'allow_null': True},
            'footer_text_tr': {'required': False},
            'footer_text_en': {'required': False},
            'social_text_tr': {'required': False},
            'social_text_en': {'required': False},
        }
    
    def to_internal_value(self, data):
        # Request'ten lang parametresini al
        request = self.context.get('request')
        lang = 'tr'  # Varsayılan
        if request:
            lang = request.query_params.get('lang', 'tr')
        
        # Boş string'leri None'a çevir ve lang'a göre map et
        if isinstance(data, dict):
            data = data.copy()
            if 'logo' in data and data['logo'] == '':
                data['logo'] = None
            
            # footer_text ve social_text'i lang'a göre map et
            if 'footer_text' in data:
                if lang == 'en' and 'footer_text_en' not in data:
                    data['footer_text_en'] = data['footer_text']
                    data.pop('footer_text', None)
                elif lang == 'tr' and 'footer_text_tr' not in data:
                    data['footer_text_tr'] = data['footer_text']
                    data.pop('footer_text', None)
            
            if 'social_text' in data:
                if lang == 'en' and 'social_text_en' not in data:
                    data['social_text_en'] = data['social_text']
                    data.pop('social_text', None)
                elif lang == 'tr' and 'social_text_tr' not in data:
                    data['social_text_tr'] = data['social_text']
                    data.pop('social_text', None)
        
        return super().to_internal_value(data)

    def get_logo_url(self, obj):
        request = self.context.get('request')
        if obj.logo and hasattr(obj.logo, 'url'):
            return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url
        return None

    def get_footer_text(self, obj):
        lang = get_language()
        if lang == 'en' and hasattr(obj, 'footer_text_en'):
            return obj.footer_text_en or obj.footer_text_tr
        return obj.footer_text_tr or obj.footer_text_en

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
    favicon = serializers.SerializerMethodField()
    
    # Mevcut ilişkiler - writable yapıyoruz
    menu_items = MenuItemSerializer(many=True, required=False)
    headers = HeaderSerializer(many=True, required=False)
    sections = GenericSectionSerializer(many=True, required=False)
    footer_policies = FooterPolicySerializer(many=True, required=False)
    social_links = SocialMediaSerializer(many=True, required=False)
    footer_info = FooterInfoSerializer(required=False)
    
    # YENİ EKLENEN İLİŞKİLER - writable yapıyoruz
    sections_our_story = GenericSectionOurStorySerializer(many=True, required=False)
    sections_contact = GenericSectionContactSerializer(many=True, required=False)
    sections_wholasale = GenericSectionWholesaleSerializer(many=True, required=False)
    faq_items = FAQItemSerializer(many=True, required=False)
    page_metas = PageMetaSerializer(many=True, required=False)

    class Meta:
        model = SiteSettings
        fields = [
            'id', 'logo', 'favicon', 
            'site_title', 'site_title_tr', 'site_title_en',
            'site_description', 'site_description_tr', 'site_description_en',
            'menu_items', 'headers', 'sections',
            'footer_policies', 'social_links', 'footer_info',
            'sections_our_story', 'sections_contact', 'sections_wholasale',
            'faq_items', 'page_metas',
        ]
        extra_kwargs = {
            'favicon': {'write_only': True, 'required': False, 'allow_null': True},
            'logo': {'write_only': True, 'required': False, 'allow_null': True},
            'site_title_tr': {'required': False},
            'site_title_en': {'required': False},
            'site_description_tr': {'required': False},
            'site_description_en': {'required': False},
        }

    def get_logo(self, obj):
        request = self.context.get('request')
        if obj.logo and hasattr(obj.logo, 'url'):
            return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url
        return None

    def get_favicon(self, obj):
        request = self.context.get('request')
        if obj.favicon and hasattr(obj.favicon, 'url'):
            return request.build_absolute_uri(obj.favicon.url) if request else obj.favicon.url
        return None

    def _clean_empty_strings(self, data):
        """Boş string'leri None'a çevir (dosya alanları için)"""
        if isinstance(data, dict):
            cleaned = {}
            for k, v in data.items():
                # Dosya alanları için boş string'leri None'a çevir
                if k in ['image', 'mobile_image', 'subimage', 'logo', 'favicon'] and isinstance(v, str) and v == '':
                    cleaned[k] = None
                elif isinstance(v, str) and v == '':
                    # Diğer alanlar için de None'a çevir (opsiyonel)
                    cleaned[k] = None
                elif isinstance(v, (dict, list)):
                    cleaned[k] = self._clean_empty_strings(v)
                else:
                    cleaned[k] = v
            return cleaned
        elif isinstance(data, list):
            return [self._clean_empty_strings(item) for item in data]
        return data

    def to_internal_value(self, data):
        # Önce boş string'leri temizle
        data = self._clean_empty_strings(data)
        # Request'ten lang parametresini al
        request = self.context.get('request')
        lang = 'tr'  # Varsayılan
        if request:
            lang = request.query_params.get('lang', 'tr')
        
        # site_title ve site_description'i lang'a göre map et ve orijinal alanları kaldır
        if isinstance(data, dict):
            data = data.copy()
            if 'site_title' in data:
                if lang == 'en' and 'site_title_en' not in data:
                    data['site_title_en'] = data['site_title']
                    # site_title alanını kaldır (sadece site_title_en kullanılacak)
                    data.pop('site_title', None)
                elif lang == 'tr' and 'site_title_tr' not in data:
                    data['site_title_tr'] = data['site_title']
                    # site_title alanını kaldır (sadece site_title_tr kullanılacak)
                    data.pop('site_title', None)
            if 'site_description' in data:
                if lang == 'en' and 'site_description_en' not in data:
                    data['site_description_en'] = data['site_description']
                    # site_description alanını kaldır (sadece site_description_en kullanılacak)
                    data.pop('site_description', None)
                elif lang == 'tr' and 'site_description_tr' not in data:
                    data['site_description_tr'] = data['site_description']
                    # site_description alanını kaldır (sadece site_description_tr kullanılacak)
                    data.pop('site_description', None)
        # Sonra normal validation'ı çalıştır
        return super().to_internal_value(data)

    def create(self, validated_data):
        # Request'ten lang parametresini al (nested serializer'lar için)
        request = self.context.get('request')
        lang = 'tr'
        if request:
            lang = request.query_params.get('lang', 'tr')
        
        # Nested data'yı çıkar
        menu_items_data = validated_data.pop('menu_items', [])
        headers_data = validated_data.pop('headers', [])
        sections_data = validated_data.pop('sections', [])
        footer_policies_data = validated_data.pop('footer_policies', [])
        social_links_data = validated_data.pop('social_links', [])
        footer_info_data = validated_data.pop('footer_info', None)
        sections_our_story_data = validated_data.pop('sections_our_story', [])
        sections_contact_data = validated_data.pop('sections_contact', [])
        sections_wholasale_data = validated_data.pop('sections_wholasale', [])
        faq_items_data = validated_data.pop('faq_items', [])

        # Ana SiteSettings objesini oluştur
        site_settings = SiteSettings.objects.create(**validated_data)

        # Menu items oluştur
        for item_data in menu_items_data:
            # text'i text_tr'ye map et
            text = item_data.pop('text', None)
            if text:
                item_data['text_tr'] = text
            MenuItem.objects.create(site=site_settings, **item_data)

        # Headers oluştur
        for header_data in headers_data:
            Header.objects.create(site=site_settings, **header_data)

        # Sections oluştur
        for section_data in sections_data:
            # product_1, product_2, product_3'ü çıkar (ForeignKey olduğu için)
            product_1 = section_data.pop('product_1', None)
            product_2 = section_data.pop('product_2', None)
            product_3 = section_data.pop('product_3', None)
            section = GenericSection.objects.create(site=site_settings, **section_data)
            if product_1:
                # Eğer dict ise ID'yi al, yoksa direkt ID olarak kullan
                product_1_id = product_1.get('id') if isinstance(product_1, dict) else (product_1.id if hasattr(product_1, 'id') else product_1)
                if product_1_id:
                    section.product_1_id = product_1_id
            if product_2:
                product_2_id = product_2.get('id') if isinstance(product_2, dict) else (product_2.id if hasattr(product_2, 'id') else product_2)
                if product_2_id:
                    section.product_2_id = product_2_id
            if product_3:
                product_3_id = product_3.get('id') if isinstance(product_3, dict) else (product_3.id if hasattr(product_3, 'id') else product_3)
                if product_3_id:
                    section.product_3_id = product_3_id
            section.save()

        # Footer policies oluştur
        for policy_data in footer_policies_data:
            FooterPolicy.objects.create(site=site_settings, **policy_data)

        # Social links oluştur
        for social_data in social_links_data:
            SocialMedia.objects.create(site=site_settings, **social_data)

        # Footer info oluştur
        if footer_info_data:
            # footer_text ve social_text'i footer_text_tr ve social_text_tr'ye map et
            footer_text = footer_info_data.pop('footer_text', None)
            social_text = footer_info_data.pop('social_text', None)
            if footer_text:
                footer_info_data['footer_text_tr'] = footer_text
            if social_text:
                footer_info_data['social_text_tr'] = social_text
            FooterInfo.objects.create(site=site_settings, **footer_info_data)

        # Sections our story oluştur
        for story_data in sections_our_story_data:
            GenericSectionOurStory.objects.create(site=site_settings, **story_data)

        # Sections contact oluştur
        for contact_data in sections_contact_data:
            # Nested address ve mail data'sını çıkar
            addresses_data = contact_data.pop('sections_address', [])
            mails_data = contact_data.pop('sections_mails', [])
            contact = GenericSectionContact.objects.create(site=site_settings, **contact_data)
            # Addresses oluştur
            for addr_data in addresses_data:
                ContactAddresses.objects.create(contact=contact, **addr_data)
            # Mails oluştur
            for mail_data in mails_data:
                ContactMails.objects.create(contact=contact, **mail_data)

        # Sections wholesale oluştur
        for wholesale_data in sections_wholasale_data:
            GenericSectionWholesale.objects.create(site=site_settings, **wholesale_data)

        # FAQ items oluştur
        for faq_data in faq_items_data:
            FAQItem.objects.create(site=site_settings, **faq_data)

        # Page metas oluştur
        for page_meta_data in page_metas_data:
            PageMeta.objects.create(site=site_settings, **page_meta_data)

        return site_settings

    def update(self, instance, validated_data):
        # Boş string'leri temizle
        validated_data = self._clean_empty_strings(validated_data)
        
        # Nested data'yı çıkar
        menu_items_data = validated_data.pop('menu_items', None)
        headers_data = validated_data.pop('headers', None)
        sections_data = validated_data.pop('sections', None)
        footer_policies_data = validated_data.pop('footer_policies', None)
        social_links_data = validated_data.pop('social_links', None)
        footer_info_data = validated_data.pop('footer_info', None)
        sections_our_story_data = validated_data.pop('sections_our_story', None)
        sections_contact_data = validated_data.pop('sections_contact', None)
        sections_wholasale_data = validated_data.pop('sections_wholasale', None)
        faq_items_data = validated_data.pop('faq_items', None)
        page_metas_data = validated_data.pop('page_metas', None)

        # Ana alanları güncelle
        instance.site_title = validated_data.get('site_title', instance.site_title)
        instance.site_description = validated_data.get('site_description', instance.site_description)
        if 'favicon' in validated_data:
            instance.favicon = validated_data['favicon']
        if 'logo' in validated_data:
            instance.logo = validated_data['logo']
        instance.save()

        # Menu items güncelle
        if menu_items_data is not None:
            # Mevcut menu item objelerini al
            existing_menu_items = list(instance.menu_items.all())
            
            for idx, item_data in enumerate(menu_items_data):
                # Eğer mevcut obje varsa güncelle, yoksa yeni oluştur
                if idx < len(existing_menu_items):
                    menu_item = existing_menu_items[idx]
                    # Sadece gönderilen alanları güncelle, diğerlerini koru
                    for key, value in item_data.items():
                        if value is not None:  # None olmayan değerleri güncelle
                            setattr(menu_item, key, value)
                    menu_item.save()
                else:
                    # Yeni obje oluştur
                    MenuItem.objects.create(site=instance, **item_data)

        # Headers güncelle
        if headers_data is not None:
            # Mevcut header objelerini al
            existing_headers = list(instance.headers.all())
            
            for idx, header_data in enumerate(headers_data):
                # Eğer mevcut obje varsa güncelle, yoksa yeni oluştur
                if idx < len(existing_headers):
                    header = existing_headers[idx]
                    # Sadece gönderilen alanları güncelle, diğerlerini koru
                    for key, value in header_data.items():
                        if value is not None:  # None olmayan değerleri güncelle
                            setattr(header, key, value)
                    header.save()
                else:
                    # Yeni obje oluştur
                    Header.objects.create(site=instance, **header_data)

        # Sections güncelle
        if sections_data is not None:
            # Mevcut section objelerini al
            existing_sections = list(instance.sections.all())
            
            for idx, section_data in enumerate(sections_data):
                product_1 = section_data.pop('product_1', None)
                product_2 = section_data.pop('product_2', None)
                product_3 = section_data.pop('product_3', None)
                
                # Eğer mevcut obje varsa güncelle, yoksa yeni oluştur
                if idx < len(existing_sections):
                    section = existing_sections[idx]
                    # Sadece gönderilen alanları güncelle, diğerlerini koru
                    for key, value in section_data.items():
                        if value is not None:  # None olmayan değerleri güncelle
                            setattr(section, key, value)
                    section.save()
                else:
                    # Yeni obje oluştur
                    section = GenericSection.objects.create(site=instance, **section_data)
                
                # Product'ları güncelle (sadece gönderildiyse)
                if product_1 is not None:
                    product_1_id = product_1.get('id') if isinstance(product_1, dict) else (product_1.id if hasattr(product_1, 'id') else product_1)
                    section.product_1_id = product_1_id if product_1_id else None
                if product_2 is not None:
                    product_2_id = product_2.get('id') if isinstance(product_2, dict) else (product_2.id if hasattr(product_2, 'id') else product_2)
                    section.product_2_id = product_2_id if product_2_id else None
                if product_3 is not None:
                    product_3_id = product_3.get('id') if isinstance(product_3, dict) else (product_3.id if hasattr(product_3, 'id') else product_3)
                    section.product_3_id = product_3_id if product_3_id else None
                section.save()

        # Footer policies güncelle
        if footer_policies_data is not None:
            # Mevcut policy objelerini al
            existing_policies = list(instance.footer_policies.all())
            
            for idx, policy_data in enumerate(footer_policies_data):
                # Eğer mevcut obje varsa güncelle, yoksa yeni oluştur
                if idx < len(existing_policies):
                    policy = existing_policies[idx]
                    # Sadece gönderilen alanları güncelle, diğerlerini koru
                    for key, value in policy_data.items():
                        if value is not None:  # None olmayan değerleri güncelle
                            setattr(policy, key, value)
                    policy.save()
                else:
                    # Yeni obje oluştur
                    FooterPolicy.objects.create(site=instance, **policy_data)

        # Social links güncelle
        if social_links_data is not None:
            instance.social_links.all().delete()
            for social_data in social_links_data:
                SocialMedia.objects.create(site=instance, **social_data)

        # Footer info güncelle
        if footer_info_data is not None:
            # Mevcut footer_info varsa güncelle, yoksa oluştur
            if hasattr(instance, 'footer_info'):
                footer_info = instance.footer_info
                # Sadece gönderilen alanları güncelle, diğerlerini koru
                for key, value in footer_info_data.items():
                    if value is not None:  # None olmayan değerleri güncelle
                        setattr(footer_info, key, value)
                footer_info.save()
            else:
                # Yeni obje oluştur
                FooterInfo.objects.create(site=instance, **footer_info_data)

        # Sections our story güncelle
        if sections_our_story_data is not None:
            # Mevcut story objelerini al
            existing_stories = list(instance.sections_our_story.all())
            
            for idx, story_data in enumerate(sections_our_story_data):
                # Eğer mevcut obje varsa güncelle, yoksa yeni oluştur
                if idx < len(existing_stories):
                    story = existing_stories[idx]
                    # Sadece gönderilen alanları güncelle, diğerlerini koru
                    for key, value in story_data.items():
                        if value is not None:  # None olmayan değerleri güncelle
                            setattr(story, key, value)
                    story.save()
                else:
                    # Yeni obje oluştur
                    GenericSectionOurStory.objects.create(site=instance, **story_data)

        # Sections contact güncelle
        if sections_contact_data is not None:
            # Mevcut contact objelerini al
            existing_contacts = list(instance.sections_contact.all())
            
            for idx, contact_data in enumerate(sections_contact_data):
                addresses_data = contact_data.pop('sections_address', [])
                mails_data = contact_data.pop('sections_mails', [])
                
                # Eğer mevcut obje varsa güncelle, yoksa yeni oluştur
                if idx < len(existing_contacts):
                    contact = existing_contacts[idx]
                    # Sadece gönderilen alanları güncelle, diğerlerini koru
                    for key, value in contact_data.items():
                        if value is not None:  # None olmayan değerleri güncelle
                            setattr(contact, key, value)
                    contact.save()
                else:
                    # Yeni obje oluştur
                    contact = GenericSectionContact.objects.create(site=instance, **contact_data)
                
                # Addresses güncelle
                existing_addresses = list(contact.sections_address.all())
                for addr_idx, addr_data in enumerate(addresses_data):
                    if addr_idx < len(existing_addresses):
                        addr = existing_addresses[addr_idx]
                        # Sadece gönderilen alanları güncelle
                        for key, value in addr_data.items():
                            if value is not None:
                                setattr(addr, key, value)
                        addr.save()
                    else:
                        ContactAddresses.objects.create(contact=contact, **addr_data)
                
                # Mails güncelle
                existing_mails = list(contact.sections_mails.all())
                for mail_idx, mail_data in enumerate(mails_data):
                    if mail_idx < len(existing_mails):
                        mail = existing_mails[mail_idx]
                        # Sadece gönderilen alanları güncelle
                        for key, value in mail_data.items():
                            if value is not None:
                                setattr(mail, key, value)
                        mail.save()
                    else:
                        ContactMails.objects.create(contact=contact, **mail_data)

        # Sections wholesale güncelle
        if sections_wholasale_data is not None:
            # Mevcut wholesale objelerini al
            existing_wholesale = list(instance.sections_wholasale.all())
            
            for idx, wholesale_data in enumerate(sections_wholasale_data):
                # Eğer mevcut obje varsa güncelle, yoksa yeni oluştur
                if idx < len(existing_wholesale):
                    wholesale = existing_wholesale[idx]
                    # Sadece gönderilen alanları güncelle, diğerlerini koru
                    for key, value in wholesale_data.items():
                        if value is not None:  # None olmayan değerleri güncelle
                            setattr(wholesale, key, value)
                    wholesale.save()
                else:
                    # Yeni obje oluştur
                    GenericSectionWholesale.objects.create(site=instance, **wholesale_data)

        # FAQ items güncelle
        if faq_items_data is not None:
            # Mevcut FAQ objelerini al
            existing_faqs = list(instance.faq_items.all())
            
            for idx, faq_data in enumerate(faq_items_data):
                # Eğer mevcut obje varsa güncelle, yoksa yeni oluştur
                if idx < len(existing_faqs):
                    faq = existing_faqs[idx]
                    # Sadece gönderilen alanları güncelle, diğerlerini koru
                    for key, value in faq_data.items():
                        if value is not None:  # None olmayan değerleri güncelle
                            setattr(faq, key, value)
                    faq.save()
                else:
                    # Yeni obje oluştur
                    FAQItem.objects.create(site=instance, **faq_data)

        # Page metas güncelle
        if page_metas_data is not None:
            # Mevcut page meta objelerini al
            existing_page_metas = {pm.page: pm for pm in instance.page_metas.all()}
            
            for page_meta_data in page_metas_data:
                page = page_meta_data.get('page')
                if page and page in existing_page_metas:
                    # Mevcut obje varsa güncelle
                    page_meta = existing_page_metas[page]
                    # Sadece gönderilen alanları güncelle, diğerlerini koru
                    for key, value in page_meta_data.items():
                        if value is not None and key != 'page':  # page alanını güncelleme
                            setattr(page_meta, key, value)
                    page_meta.save()
                elif page:
                    # Yeni obje oluştur
                    PageMeta.objects.create(site=instance, **page_meta_data)

        return instance

