from django.conf import settings
from cryptography.fernet import Fernet, InvalidToken

def get_fernet():
    """
    settings.py'deki FERNET_KEY'i kullanarak bir Fernet instance'ı oluşturur.
    """
    key = getattr(settings, 'FERNET_KEY', None)
    if not key:
        raise ValueError("Şifreleme için FERNET_KEY ayarı settings.py dosyasında bulunamadı.")
    return Fernet(key)

def encrypt_value(value: str) -> str:
    """
    Verilen bir metni şifreler.
    """
    f = get_fernet()
    return f.encrypt(value.encode()).decode()

def decrypt_value(encrypted_value: str) -> str:
    """
    Şifrelenmiş bir metni çözer.
    """
    if not encrypted_value:
        return ""
    f = get_fernet()
    try:
        return f.decrypt(encrypted_value.encode()).decode()
    except (InvalidToken, TypeError):
        # Değer şifreli değilse veya anahtar yanlışsa boş döner.
        # Bu, ham metnin yanlışlıkla çözülmeye çalışılmasını engeller.
        return ""
