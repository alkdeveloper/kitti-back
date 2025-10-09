from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import ContactFormEntry
from django.conf import settings

@receiver(post_save, sender=ContactFormEntry)
def send_contact_email(sender, instance, created, **kwargs):
    if created:
        try:
            subject = f"Yeni İletişim Formu Mesajı: {instance.name}"
            message_body = f"""
            Ad Soyad: {instance.name}
            E-posta: {instance.email}
            Telefon: {instance.phone or 'Belirtilmedi'}
            
            Mesaj:
            {instance.message}
            
            ---
            Kampanya ve duyuruları kabul etti mi?: {'Evet' if instance.subscribe_newsletter else 'Hayır'}
            """
            EMAIL_HOST_USER = getattr(settings, 'EMAIL_HOST_USER', None)
            EMAIL_HOST_PASSWORD = getattr(settings, 'EMAIL_HOST_PASSWORD', None)
            RECIEPENT_EMAIL = getattr(settings, 'RECIEPENT_EMAIL', None)
            send_mail(
                subject=subject,
                message=message_body,
                from_email=EMAIL_HOST_USER,
                recipient_list=[RECIEPENT_EMAIL],
                auth_user=EMAIL_HOST_USER,
                # DEĞİŞİKLİK: Şifreyi çözen property'yi kullanıyoruz.
                auth_password=EMAIL_HOST_PASSWORD,
                fail_silently=False,
                connection=None
            )
            
            instance.is_sent = True
            instance.save(update_fields=['is_sent'])

        except Exception as e:
            print(f"HATA: E-posta gönderilemedi. Detay: {e}")

