from rest_framework import serializers
from .models import ContactFormEntry

class ContactFormEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactFormEntry
        fields = [
            'name', 
            'email', 
            'phone', 
            'message', 
            'accept_terms', 
            'subscribe_newsletter'
        ]
    
    def validate_accept_terms(self, value):
        """
        'accept_terms' alanının 'True' olması gerektiğini doğrular.
        """
        if not value:
            raise serializers.ValidationError("Kişisel verilerinizin işlenmesini kabul etmelisiniz.")
        return value
