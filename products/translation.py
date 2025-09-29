# products/translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import Item, Slider

@register(Item)
class ItemTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(Slider)
class SliderTranslationOptions(TranslationOptions):
    fields = ('title',)