from modeltranslation.translator import register, TranslationOptions
from .models import (
    SiteSettings, Header, GenericSectionOurStory, GenericSectionContact,
    GenericSection, FooterPolicy, FooterInfo, MenuItem, ContactAddresses, GenericSectionWholesale
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
    fields = ('title', 'description')

@register(FooterInfo)
class FooterInfoTranslationOptions(TranslationOptions):
    fields = ('footer_text', 'social_text')

@register(GenericSectionOurStory)
class GenericSectionOurStoryTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'subtitle',
        'title',
        'description',
        'subimage', # Bu alanın metin içerdiği varsayıldı
        'button_text',
    )

@register(GenericSectionContact)
class GenericSectionContactTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(ContactAddresses)
class ContactAddressesTranslationOptions(TranslationOptions):
    fields = ('title', 'description',) # tel ve tel_wp alanları çevrilmez

@register(GenericSectionWholesale)
class GenericSectionWholesaleTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'description',
        'info_text',
        'button_top_title',
        'button_top_text',
        'button_bottom_title',
        'button_bottom_text',
    )

