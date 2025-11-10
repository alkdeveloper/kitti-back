from django.urls import path
from .views import ContactFormCreateView

urlpatterns = [
    path('contact/submit/', ContactFormCreateView.as_view(), name='contact-submit'),
]

