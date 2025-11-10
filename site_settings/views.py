from rest_framework import viewsets
from .models import *
from .serializers import *
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.utils.translation import activate # activate fonksiyonunu import ediyoruz

# ViewSet için genel etiketleme
@extend_schema(tags=['Site Ayarları'])
class SiteSettingsViewSet(viewsets.ModelViewSet):
    """
    Site genel ayarlarını (başlık, logo, menü, header, footer vb.) yönetmek için kullanılan API endpoint'leri.
    `lang` query parametresi ile dil seçimi yapılabilir (tr/en). Varsayılan dil Türkçe'dir.
    """
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer

    @extend_schema(
        summary="Site Ayarlarını Listele",
        description="Sistemdeki site ayarları yapılandırmasını getirir. Genellikle sadece bir tane olacaktır.",
        parameters=[
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Dil kodu (tr/en)',
                enum=['tr', 'en'],
                default='tr'
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        # 1. URL'den 'lang' parametresini al, eğer yoksa 'tr' olarak varsay.
        lang = request.query_params.get('lang', 'tr')
        
        # 2. Geçerli bir dil kodu ise, o dili aktif et.
        if lang in ['tr', 'en']:
            activate(lang)
            
        # 3. Geri kalan işlemleri DRF'in standart list metoduna bırak.
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Tek Bir Site Ayarını Getir",
        description="Belirtilen ID'ye sahip site ayarları yapılandırmasını detaylarıyla birlikte getirir.",
        parameters=[
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Dil kodu (tr/en)',
                enum=['tr', 'en'],
                default='tr'
            ),
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        # Liste metodundaki mantığın aynısını tekil getirme işlemi için de uygula
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        
        return super().retrieve(request, *args, **kwargs)

