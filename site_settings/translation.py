from modeltranslation.translator import register, TranslationOptions
from .models import (
    SiteSettings, Header,
    GenericSection, FooterPolicy, FooterInfo, MenuItem
)

@register(MenuItem)
class MenuItemTranslationOptions(TranslationOptions):
    fields = ('text',)

@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    fields = ('site_title', 'site_description',)

@register(Header)
class HeaderTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(GenericSection)
class GenericSectionTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'subtitle',
        'title',
        'description',
        'button_text_left',
        'button_text_right',
    )

@register(FooterPolicy)
class FooterPolicyTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(FooterInfo)
class FooterInfoTranslationOptions(TranslationOptions):
    fields = ('footer_text',)