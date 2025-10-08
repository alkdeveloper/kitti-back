from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.forms import TextInput, Textarea
from modeltranslation.admin import TranslationAdmin
from .models import (
    SiteSettings, Header, MenuItem,
    GenericSection, FooterPolicy, FooterInfo, SocialMedia
)

# ------------------------
# YENİ EKLENDİ: Inline: Menü Elemanları
# ------------------------
class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('text', 'href')
    verbose_name = "Menü Elemanı"
    verbose_name_plural = "Menü Elemanları"

# ------------------------
# Inline: Footer Policy
# ------------------------
class FooterPolicyInline(admin.TabularInline):
    model = FooterPolicy
    extra = 1
    fields = ('title', 'description')
    verbose_name = "Aydınlatma / Politika"
    verbose_name_plural = "Aydınlatma / Politikalar"

# ------------------------
# Inline: Sosyal Medya Linkleri
# ------------------------
class SocialMediaLinkInline(admin.TabularInline):
    model = SocialMedia
    extra = 1
    fields = ('icon', 'url')
    verbose_name = "Sosyal Medya Linki"
    verbose_name_plural = "Sosyal Medya Linkleri"

# ------------------------
# Base Translation Admin
# ------------------------
class BaseTranslationAdmin(TranslationAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 100})},
    }

# ------------------------
# Site Settings Admin
# ------------------------
@admin.register(SiteSettings)
class SiteSettingsAdmin(BaseTranslationAdmin):
    list_display = ('site_title', 'logo',)
    fieldsets = (
        (_("Genel Bilgiler"), {
            'fields': ('site_title', 'site_description', 'logo')
        }),
    )
    inlines = [MenuItemInline, FooterPolicyInline, SocialMediaLinkInline]

# ------------------------
# Header Admin
# ------------------------
@admin.register(Header)
class HeaderAdmin(BaseTranslationAdmin):
    list_display = ('title', 'description')
    fieldsets = (
        (_("Header Bilgileri"), {
            'fields': ('title', 'description', 'image')
        }),
    )

# ------------------------
# Generic Section Admin
# ------------------------
@admin.register(GenericSection)
class GenericSectionAdmin(BaseTranslationAdmin):
    list_display = ('name', 'type', 'title_tr', 'title_en')
    list_filter = ('type',)
    fieldsets = (
        (_("Genel Bilgiler"), {
            'fields': ('type', 'name', 'subtitle_tr', 'subtitle_en', 'title_tr', 'title_en', 'description_tr', 'description_en', 'image')
        }),
        (_("Buton Bilgileri"), {
            'fields': (
                'button_text_left_tr', 'button_text_left_en', 'button_url_left',
                'button_text_right_tr', 'button_text_right_en', 'button_url_right',
            ),
        }),
        (_("Favoriler (sadece 'Favorites of Season' için)"), {
            'fields': ('product_1', 'product_2', 'product_3'),
        }),
    )

# ------------------------
# Footer Admin
# ------------------------
@admin.register(FooterInfo)
class FooterAdmin(BaseTranslationAdmin):
    list_display = ('logo',)
    fieldsets = (
        (_("Footer Genel Bilgiler"), {
            'fields': ('logo', 'footer_text',)
        }),
    )

