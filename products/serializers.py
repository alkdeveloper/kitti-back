# products/serializers.py
from rest_framework import serializers
from .models import Item, ItemImage, Slider
from django.utils.translation import get_language

class ItemImageSerializer(serializers.ModelSerializer):
    """Ürün resim serializer"""
    
    class Meta:
        model = ItemImage
        fields = ['id', 'image']
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True},
        }

class ProductSerializer(serializers.ModelSerializer):
    """Ürün serializer"""
    images = ItemImageSerializer(many=True, required=False)
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = Item
        fields = [
            'id', 'title', 'title_tr', 'title_en',
            'description', 'description_tr', 'description_en',
            'icon', 'images', 'parent', 'item_type',
            'level', 'lft', 'rght'
        ]
        extra_kwargs = {
            'icon': {'write_only': True, 'required': False, 'allow_null': True},
            'title_tr': {'required': False},
            'title_en': {'required': False},
            'description_tr': {'required': False},
            'description_en': {'required': False},
            'parent': {'required': False, 'allow_null': True},
        }
    
    def get_title(self, obj):
        """Aktif dile göre title döndür"""
        language = get_language()
        if language == 'en':
            return obj.title_en or obj.title_tr
        return obj.title_tr or obj.title_en
    
    def get_description(self, obj):
        """Aktif dile göre description döndür"""
        language = get_language()
        if language == 'en':
            return obj.description_en or obj.description_tr
        return obj.description_tr or obj.description_en
    
    def to_internal_value(self, data):
        # Request'ten lang parametresini al
        request = self.context.get('request')
        lang = 'tr'  # Varsayılan
        if request:
            lang = request.query_params.get('lang', 'tr')
        
        # Boş string'leri None'a çevir ve lang'a göre map et
        if isinstance(data, dict):
            data = data.copy()
            if 'icon' in data and data['icon'] == '':
                data['icon'] = None
            
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
            
            # parent'ı ID'ye çevir
            if 'parent' in data:
                if isinstance(data['parent'], dict):
                    data['parent'] = data['parent'].get('id')
        
        return super().to_internal_value(data)
    
    def create(self, validated_data):
        # item_type'ı product olarak ayarla
        validated_data['item_type'] = 'product'
        # images'ı çıkar (nested olarak işlenecek)
        images_data = validated_data.pop('images', [])
        item = Item.objects.create(**validated_data)
        
        # Images oluştur
        for image_data in images_data:
            if image_data and image_data.get('image'):
                ItemImage.objects.create(item=item, image=image_data['image'])
        
        return item
    
    def update(self, instance, validated_data):
        # images'ı çıkar
        images_data = validated_data.pop('images', None)
        
        # Ana alanları güncelle
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        
        # Images güncelle (mevcut images'ı sil, yenilerini ekle)
        if images_data is not None:
            instance.images.all().delete()
            for image_data in images_data:
                if image_data and image_data.get('image'):
                    ItemImage.objects.create(item=instance, image=image_data['image'])
        
        return instance

class CategorySerializer(serializers.ModelSerializer):
    """Kategori serializer"""
    products = ProductSerializer(many=True, read_only=True)
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Item
        fields = [
            'id', 'title', 'title_tr', 'title_en',
            'description', 'description_tr', 'description_en',
            'icon', 'category_type', 'parent', 'item_type',
            'products', 'products_count', 'level', 'lft', 'rght'
        ]
        extra_kwargs = {
            'icon': {'write_only': True, 'required': False, 'allow_null': True},
            'title_tr': {'required': False},
            'title_en': {'required': False},
            'description_tr': {'required': False},
            'description_en': {'required': False},
            'parent': {'required': False, 'allow_null': True},
            'category_type': {'required': False, 'allow_null': True},
        }
    
    def get_title(self, obj):
        """Aktif dile göre title döndür"""
        language = get_language()
        if language == 'en':
            return obj.title_en or obj.title_tr
        return obj.title_tr or obj.title_en
    
    def get_description(self, obj):
        """Aktif dile göre description döndür"""
        language = get_language()
        if language == 'en':
            return obj.description_en or obj.description_tr
        return obj.description_tr or obj.description_en
    
    def get_products_count(self, obj):
        """Kategorideki ürün sayısı"""
        return obj.children.filter(item_type='product').count()
    
    def to_internal_value(self, data):
        # Request'ten lang parametresini al
        request = self.context.get('request')
        lang = 'tr'  # Varsayılan
        if request:
            lang = request.query_params.get('lang', 'tr')
        
        # Boş string'leri None'a çevir ve lang'a göre map et
        if isinstance(data, dict):
            data = data.copy()
            if 'icon' in data and data['icon'] == '':
                data['icon'] = None
            
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
            
            # parent'ı ID'ye çevir
            if 'parent' in data:
                if isinstance(data['parent'], dict):
                    data['parent'] = data['parent'].get('id')
        
        return super().to_internal_value(data)
    
    def create(self, validated_data):
        # item_type'ı category olarak ayarla
        validated_data['item_type'] = 'category'
        category = Item.objects.create(**validated_data)
        return category
    
    def update(self, instance, validated_data):
        # Ana alanları güncelle
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

class CategoryWithProductsSerializer(serializers.ModelSerializer):
    """MPTT tree yapısında kategori ve ürünleri"""
    children = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = Item
        fields = [
            'id', 'title', 'description', 'icon', 'category_type',
            'item_type', 'level', 'children'
        ]
    
    def get_title(self, obj):
        language = get_language()
        if language == 'en':
            return obj.title_en or obj.title_tr
        return obj.title_tr or obj.title_en
    
    def get_description(self, obj):
        language = get_language()
        if language == 'en':
            return obj.description_en or obj.description_tr
        return obj.description_tr or obj.description_en
    
    def get_children(self, obj):
        """Alt kategorileri ve ürünleri getir"""
        children = obj.get_children()
        
        # Kategorileri ve ürünleri ayır
        categories = children.filter(item_type='category')
        products = children.filter(item_type='product')
        
        result = []
        
        # Alt kategorileri ekle (recursive)
        for category in categories:
            result.append(CategoryWithProductsSerializer(category, context=self.context).data)
        
        # Ürünleri ekle
        for product in products:
            result.append(ProductSerializer(product, context=self.context).data)
        
        return result

class CategoryProductsSerializer(serializers.ModelSerializer):
    """Kategori ve sadece altındaki ürünleri döndüren serializer"""
    products = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    icon_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Item
        fields = [
            'id', 'title', 'title_tr', 'title_en',
            'description', 'description_tr', 'description_en',
            'icon', 'icon_url', 'category_type', 'level', 'products'
        ]
    
    def get_title(self, obj):
        language = get_language()
        if language == 'en':
            return obj.title_en or obj.title_tr
        return obj.title_tr or obj.title_en
    
    def get_description(self, obj):
        language = get_language()
        if language == 'en':
            return obj.description_en or obj.description_tr
        return obj.description_tr or obj.description_en
    
    def get_icon_url(self, obj):
        """Icon field için URL döndür"""
        request = self.context.get('request')
        if obj.icon and hasattr(obj.icon, 'url'):
            return request.build_absolute_uri(obj.icon.url) if request else obj.icon.url
        return None
    
    def get_products(self, obj):
        """Kategorinin altındaki sadece ürünleri getir"""
        products = obj.children.filter(item_type='product').order_by('lft')
        return ProductSerializer(products, many=True, context=self.context).data

class SliderSerializer(serializers.ModelSerializer):
    """Slider serializer"""
    title = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Slider
        fields = [
            'id', 'title', 'title_tr', 'title_en',
            'image', 'image_url', 'parent', 'level'
        ]
        extra_kwargs = {
            'image': {'write_only': True, 'required': False, 'allow_null': True},
            'title_tr': {'required': False},
            'title_en': {'required': False},
            'parent': {'required': False, 'allow_null': True},
        }
    
    def get_title(self, obj):
        language = get_language()
        if language == 'en':
            return obj.title_en or obj.title_tr
        return obj.title_tr or obj.title_en
    
    def get_image_url(self, obj):
        """Image field için URL döndür"""
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None
    
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
            
            # title'i lang'a göre map et
            if 'title' in data:
                if lang == 'en' and 'title_en' not in data:
                    data['title_en'] = data['title']
                    data.pop('title', None)
                elif lang == 'tr' and 'title_tr' not in data:
                    data['title_tr'] = data['title']
                    data.pop('title', None)
            
            # parent'ı ID'ye çevir
            if 'parent' in data:
                if isinstance(data['parent'], dict):
                    data['parent'] = data['parent'].get('id')
        
        return super().to_internal_value(data)