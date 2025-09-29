# products/admin.py
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.forms import TextInput, Textarea
from .models import Item, ItemImage, Slider

# ------------------------
# Item Image Inline
# ------------------------
class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1
    fields = ('image',)

# ------------------------
# Base Admin
# ------------------------
class BaseTranslationMPTTAdmin(TranslationAdmin, DraggableMPTTAdmin):
    pass

# ------------------------
# Item Admin (Tek admin ile her şeyi yönet)
# ------------------------
@admin.register(Item)
class ItemAdmin(BaseTranslationMPTTAdmin):
    inlines = [ItemImageInline]
    list_display = ('tree_actions', 'indented_title', 'item_type', 'category_type', 'id')
    list_display_links = ('indented_title',)
    list_filter = ('item_type', 'category_type')
    search_fields = ('title_tr', 'title_en', 'description_tr', 'description_en')
    
    # Item type'a göre farklı renkler için CSS
    class Media:
        css = {
            'all': ('admin/css/item_admin.css',)
        }
    
    def get_fields(self, request, obj=None):
        """Item type'a göre alanları dinamik olarak göster"""
        base_fields = ['title_tr', 'title_en', 'description_tr', 'description_en', 'icon', 'item_type']
        
        if obj:
            if obj.item_type == 'category':
                return base_fields + ['category_type', 'parent']
            elif obj.item_type == 'product':
                return base_fields + ['parent']
        
        # Yeni kayıt için tüm alanları göster
        return base_fields + ['category_type', 'parent']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Parent seçeneklerini filtrele"""
        if db_field.name == "parent":
            # Product için sadece category'leri göster
            kwargs["queryset"] = Item.objects.filter(item_type='category')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_list_display(self, request):
        """List display'i dinamik yap"""
        return ('tree_actions', 'indented_title', 'get_type_badge', 'category_type', 'id')
    
    def get_type_badge(self, obj):
        """Item type için renkli badge"""
        if obj.item_type == 'category':
            return f'📁 {obj.get_item_type_display()}'
        else:
            return f'📦 {obj.get_item_type_display()}'
    
    get_type_badge.short_description = 'Type'
    get_type_badge.allow_tags = True
    
    def get_queryset(self, request):
        """Queryset'i optimize et"""
        qs = super().get_queryset(request)
        return qs.select_related('parent')

# ------------------------
# Slider Admin
# ------------------------
@admin.register(Slider)
class SliderAdmin(BaseTranslationMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'id')
    list_display_links = ('indented_title',)
    search_fields = ('title_tr', 'title_en')
    
    # Sadece dil özel alanları göster
    fields = ('title_tr', 'title_en', 'image', 'parent')