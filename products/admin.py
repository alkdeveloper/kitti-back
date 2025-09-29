# products/admin.py
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from modeltranslation.admin import TranslationAdmin
from .models import Category, Product, ProductImage, Slider

# ------------------------
# Product Inline
# ------------------------
class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    show_change_link = True
    fields = ('title_tr', 'title_en', 'icon', 'description_tr', 'description_en')

# ------------------------
# ProductImage Inline
# ------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image',)

# ------------------------
# Base Admin (TranslationAdmin + DraggableMPTTAdmin)
# ------------------------
class BaseTranslationMPTTAdmin(TranslationAdmin, DraggableMPTTAdmin):
    pass

# ------------------------
# Category Admin
# ------------------------
@admin.register(Category)
class CategoryAdmin(BaseTranslationMPTTAdmin):
    inlines = [ProductInline]
    list_display = ('tree_actions', 'indented_title', 'type', 'id')
    list_display_links = ('indented_title',)
    search_fields = ('title_tr', 'title_en', 'description_tr', 'description_en')
    list_filter = ('type',)
    
    # Sadece dil özel alanları göster
    fields = ('title_tr', 'title_en', 'description_tr', 'description_en', 'icon', 'type', 'parent')

# ------------------------
# Product Admin
# ------------------------
@admin.register(Product)
class ProductAdmin(BaseTranslationMPTTAdmin):
    inlines = [ProductImageInline]
    list_display = ('tree_actions', 'indented_title', 'category', 'id')
    list_display_links = ('indented_title',)
    search_fields = ('title_tr', 'title_en', 'description_tr', 'description_en')
    list_filter = ('category',)
    
    # Sadece dil özel alanları göster
    fields = ('title_tr', 'title_en', 'description_tr', 'description_en', 'icon', 'category', 'parent')

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