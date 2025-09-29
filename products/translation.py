# products/translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import Category, Product, Slider

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(Slider)
class SliderTranslationOptions(TranslationOptions):
    fields = ('title',)