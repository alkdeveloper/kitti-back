from rest_framework import viewsets
from .models import *
from .serializers import *
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
@extend_schema(
        parameters=[
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Dil kodu (tr/en)',
                enum=['tr', 'en']
            ),
        ],
        responses={200: SiteSettingsSerializer(many=True)},
        description="Setting öğelerini listeler"
    )
class SiteSettingsViewSet(viewsets.ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer