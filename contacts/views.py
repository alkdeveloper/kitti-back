from rest_framework import generics
from .models import ContactFormEntry
from .serializers import ContactFormEntrySerializer

class ContactFormCreateView(generics.CreateAPIView):
    """
    Sadece POST isteklerini kabul ederek yeni bir iletişim formu mesajı oluşturur.
    """
    queryset = ContactFormEntry.objects.all()
    serializer_class = ContactFormEntrySerializer
