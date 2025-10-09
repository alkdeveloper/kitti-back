from django.db import models
# DEĞİŞİKLİK: EncryptedTextField import'u kaldırıldı.
# from cryptography.fields import EncryptedTextField
from .utils import encrypt_value, decrypt_value # Yeni yardımcı fonksiyonları import et

# ... ContactFormEntry modeli aynı kalır ...
class ContactFormEntry(models.Model):
    name = models.CharField("Ad Soyad", max_length=255)
    email = models.EmailField("E-posta Adresi")
    phone = models.CharField("Telefon Numarası", max_length=20, blank=True, null=True)
    message = models.TextField("Mesaj")
    accept_terms = models.BooleanField("Kişisel verilerin işlenmesini kabul etti")
    subscribe_newsletter = models.BooleanField("Kampanya ve duyurular hakkında bilgilendirilmek istiyor", default=False)
    is_sent = models.BooleanField("E-posta Gönderildi mi?", default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "İletişim Formu Mesajı"
        verbose_name_plural = "İletişim Formu Mesajları"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email}"

