from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from .models import (
    SiteSettings, MenuItem, Header, GenericSection,
    GenericSectionOurStory, GenericSectionContact, ContactAddresses, ContactMails,
    GenericSectionWholesale, FooterPolicy, SocialMedia, FooterInfo
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
    )

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
    list_display = ('title', 'display_image_field')
    
    def display_image_field(self, obj):
        return self.display_image(obj, 'image')
    display_image_field.short_description = _('Görsel')
    
    # İstek üzerine oluşturma ve silme engellendi.
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# -----------------------------------------------------------------------------
# Ana Sayfa Bölümleri (GenericSection - Sadece "Home Page" olan)
# -----------------------------------------------------------------------------
@admin.register(GenericSection)
class HomePageSectionAdmin(BaseTranslationAdmin):
    list_display = ('name', 'title', 'display_image_field')
    
    def display_image_field(self, obj):
        return self.display_image(obj, 'image')
    display_image_field.short_description = _('Ana Görsel')
    
    # DÜZELTME (E202): HeaderInline buradan kaldırıldı.
    inlines = []

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


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