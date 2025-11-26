from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from django.contrib.admin import TabularInline

from .models import (
    SiteSettings, MenuItem, Header, GenericSection,
    GenericSectionOurStory, GenericSectionContact, ContactAddresses, ContactMails,
    GenericSectionWholesale, FooterPolicy, SocialMedia, FooterInfo, FAQItem, PageMeta
)

# -----------------------------------------------------------------------------
# GENEL AYARLAR VE YARDIMCI FONKSİYONLAR
# -----------------------------------------------------------------------------

class BaseTranslationAdmin(TranslationAdmin):
    def display_image(self, obj, field_name='image'):
        field = getattr(obj, field_name)
        if field and hasattr(field, 'url'):
            return mark_safe(f'<img src="{field.url}" width="100" />')
        return _("Görsel Yok")
    display_image.short_description = _('Görsel Önizleme')

# -----------------------------------------------------------------------------
# Site Ayarları Admin Paneli (SiteSettings)
# -----------------------------------------------------------------------------
class PageMetaInline(TabularInline):
    """PageMeta için inline admin"""
    model = PageMeta
    extra = 0
    fields = ('page', 'meta_title_tr', 'meta_title_en', 'meta_description_tr', 'meta_description_en')
    verbose_name = "Sayfa Meta Bilgisi"
    verbose_name_plural = "Sayfa Meta Bilgileri"

@admin.register(SiteSettings)
class SiteSettingsAdmin(BaseTranslationAdmin):
    # 'favicon' için de bir önizleme alanı ekliyoruz.
    list_display = ('__str__', 'site_title', 'display_logo_field', 'display_favicon_field')
    list_editable = ('site_title',)

    # Mevcut fieldset'e 'favicon'ı ekliyoruz.
    fieldsets = (
        ("Genel Bilgiler", {
            'fields': ('site_title', 'site_description', 'logo', 'favicon')
        }),
        ("Takip Kodları", {
            'fields': ('head_tracking_code', 'body_tracking_code'),
            'description': _(
                "Google Tag (gtag.js), Meta Pixel ve benzeri global takip kodlarını buraya ekleyin. "
                "Head için olan script'leri 'Head Tracking Code' alanına, noscript/body için olanları "
                "'Body Tracking Code' alanına ekleyin."
            ),
        }),
    )
    
    inlines = [PageMetaInline]

    def display_logo_field(self, obj):
        return self.display_image(obj, 'logo')
    display_logo_field.short_description = 'Logo Önizleme'

    # Favicon için yeni önizleme fonksiyonu
    def display_favicon_field(self, obj):
        return self.display_image(obj, 'favicon')
    display_favicon_field.short_description = 'Favicon Önizleme'

    def has_delete_permission(self, request, obj=None):
        return False

# -----------------------------------------------------------------------------
# Menü Elemanları Admin Paneli (MenuItem)
# -----------------------------------------------------------------------------
@admin.register(MenuItem)
class MenuItemAdmin(BaseTranslationAdmin):
    # DÜZELTME (E124): 'list_editable' hatasını çözmek için 'id' alanını başa ekliyoruz.
    list_display = ('id', 'text', 'href', 'site')
    list_editable = ('text', 'href', 'site')
    list_filter = ('site',)
    search_fields = ('text', 'href')

# -----------------------------------------------------------------------------
# Ana Sayfa Header Yönetimi (Header)
# DÜZELTME (E202): Header modeli, GenericSection'a değil, SiteSettings'e bağlı olduğu
# için inline olarak kullanılamaz. Bu yüzden ayrı bir admin olarak kaydedildi.
# -----------------------------------------------------------------------------
@admin.register(Header)
class HeaderAdmin(BaseTranslationAdmin):
    list_display = ('id', 'title', 'display_image_field')
    list_editable = ('title',)
    search_fields = ('title', 'description')
    
    def display_image_field(self, obj):
        return self.display_image(obj, 'image')
    display_image_field.short_description = _('Görsel')

# -----------------------------------------------------------------------------
# Ana Sayfa Bölümleri (GenericSection - Sadece "Home Page" olan)
# -----------------------------------------------------------------------------
@admin.register(GenericSection)
class HomePageSectionAdmin(BaseTranslationAdmin):
    list_display = ('id', 'name', 'type', 'title', 'display_image_field')
    list_editable = ('title',)
    list_filter = ('type',)
    search_fields = ('name', 'title', 'description')
    
    def display_image_field(self, obj):
        return self.display_image(obj, 'image')
    display_image_field.short_description = _('Ana Görsel')


# ... Diğer admin sınıflarınız (GenericSectionOurStoryAdmin, GenericSectionContactAdmin) aynı kalabilir ...
# Aşağıda sadece E124 hatası veren sınıfları tekrar ekliyorum.

# -----------------------------------------------------------------------------
# Toptan Satış Sayfası Bölümleri (GenericSectionWholesale)
# -----------------------------------------------------------------------------
@admin.register(GenericSectionWholesale)
class GenericSectionWholesaleAdmin(BaseTranslationAdmin):
    # DÜZELTME (E124): '__str__' metodunu veya 'id'yi başa ekleyebiliriz.
    list_display = ('title', 'display_image_field')
    # list_editable 'title' ile başlayamaz, ama zaten tek eleman olduğu için düzenleme linki yeterlidir.
    # list_editable = ('title',) # Bu satırı kaldırarak hatayı çözebilir veya list_display'i değiştirebiliriz.

    def display_image_field(self, obj):
        return self.display_image(obj, 'image')
    display_image_field.short_description = _('Görsel')


# -----------------------------------------------------------------------------
# Footer Yönetim Panelleri
# -----------------------------------------------------------------------------

@admin.register(FooterInfo)
class FooterInfoAdmin(BaseTranslationAdmin):
    list_display = ('__str__', 'footer_text', 'social_text', 'display_logo_field')
    list_editable = ('footer_text', 'social_text')
    
    def display_logo_field(self, obj):
        return self.display_image(obj, 'logo')
    display_logo_field.short_description = _('Footer Logo')

    def has_add_permission(self, request):
        return not FooterInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(FooterPolicy)
class FooterPolicyAdmin(BaseTranslationAdmin):
    # DÜZELTME (E124): 'id' alanını başa ekliyoruz.
    list_display = ('id', 'title',)
    list_editable = ('title',)
    search_fields = ('title', 'description')

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    # DÜZELTME (E124): 'id' alanını başa ekliyoruz.
    list_display = ('id', 'icon', 'url')
    list_editable = ('icon', 'url')


# GenericSectionOurStoryAdmin ve GenericSectionContactAdmin sınıflarınızda
# E124 hatası olmadığı için onları değiştirmenize gerek yok.
# Onları bir önceki cevaptaki gibi bırakabilirsiniz.
@admin.register(GenericSectionOurStory)
class GenericSectionOurStoryAdmin(BaseTranslationAdmin):
    list_display = ('name', 'type', 'title', 'display_image_field', 'display_sub_image_field')
    list_editable = ('title',)
    list_filter = ('type',)
    search_fields = ('name', 'title', 'description')

    def display_image_field(self, obj):
        return self.display_image(obj, 'image')
    display_image_field.short_description = _('Görsel')

    def display_sub_image_field(self, obj):
        return self.display_image(obj, 'subimage')
    display_sub_image_field.short_description = _('Üst Görsel')

class ContactAddressesInline(TranslationTabularInline): # Dil desteği için TranslationTabularInline kullanıldı
    model = ContactAddresses
    extra = 1

class ContactMailsInline(admin.TabularInline):
    model = ContactMails
    extra = 1

@admin.register(GenericSectionContact)
class GenericSectionContactAdmin(BaseTranslationAdmin):
    list_display = ('title',)
    inlines = [ContactAddressesInline, ContactMailsInline]

# -----------------------------------------------------------------------------
# FAQ (Sıkça Sorulan Sorular) Admin Paneli
# -----------------------------------------------------------------------------
@admin.register(FAQItem)
class FAQItemAdmin(BaseTranslationAdmin):
    list_display = ('id', 'question', 'order')
    list_editable = ('order',)
    list_filter = ('site',)
    search_fields = ('question', 'answer')
    ordering = ['order', 'id']

# -----------------------------------------------------------------------------
# Page Meta (Sayfa Meta Bilgileri) Admin Paneli
# SiteSettings içinde inline olarak gösteriliyor, ayrı admin paneli opsiyonel
# -----------------------------------------------------------------------------
@admin.register(PageMeta)
class PageMetaAdmin(admin.ModelAdmin):
    list_display = ('id', 'page', 'meta_title_tr', 'meta_title_en')
    list_filter = ('site', 'page')
    search_fields = ('meta_title_tr', 'meta_title_en', 'meta_description_tr', 'meta_description_en')
    ordering = ['page']
    
    fieldsets = (
        ('Sayfa Bilgisi', {
            'fields': ('site', 'page')
        }),
        ('Meta Title (Türkçe)', {
            'fields': ('meta_title_tr',)
        }),
        ('Meta Title (İngilizce)', {
            'fields': ('meta_title_en',)
        }),
        ('Meta Description (Türkçe)', {
            'fields': ('meta_description_tr',)
        }),
        ('Meta Description (İngilizce)', {
            'fields': ('meta_description_en',)
        }),
    )

