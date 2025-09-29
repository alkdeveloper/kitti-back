# products/serializers.py
from rest_framework import serializers
from .models import Item, ItemImage, Slider
from django.utils.translation import get_language

class ItemImageSerializer(serializers.ModelSerializer):
    """Ürün resim serializer"""
    
    class Meta:
        model = ItemImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    """Ürün serializer"""
    images = ItemImageSerializer(many=True, read_only=True)
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = Item
        fields = [
            'id', 'title', 'description', 'icon', 
            'images', 'level', 'lft', 'rght'
        ]
    
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

class CategorySerializer(serializers.ModelSerializer):
    """Kategori serializer"""
    products = ProductSerializer(many=True, read_only=True)
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Item
        fields = [
            'id', 'title', 'description', 'icon', 'category_type',
            'products', 'products_count', 'level', 'lft', 'rght'
        ]
    
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

# Slider için de model eklemeniz gerekiyor, şimdilik Item modelini kullanacağız
class SliderSerializer(serializers.ModelSerializer):
    """Slider serializer"""
    title = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Slider
        fields = ['id', 'title', 'image', 'level']
    
    def get_title(self, obj):
        language = get_language()
        if language == 'en':
            return obj.title_en or obj.title_tr
        return obj.title_tr or obj.title_en
    
    def get_image(self, obj):
        """Image field için URL döndür"""
        language = get_language()
        request = self.context.get('request')
        
        # Dile göre image field seç
        image_field = None
        if language == 'en':
            image_field = obj.image_en or obj.image_tr
        else:
            image_field = obj.image_tr or obj.image_en
        
        # Image varsa tam URL döndür
        if image_field:
            if request:
                return request.build_absolute_uri(image_field.url)
            return image_field.url
        return None