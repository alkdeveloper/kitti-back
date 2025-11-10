from django.contrib import admin
from .models import ContactFormEntry

@admin.register(ContactFormEntry)
class ContactFormEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_sent', 'created_at')
    list_filter = ('is_sent', 'subscribe_newsletter', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'phone', 'message', 'accept_terms', 'subscribe_newsletter', 'created_at', 'is_sent')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

