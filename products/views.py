# products/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.utils.translation import activate
from .models import Item
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    CategoryWithProductsSerializer,
    SliderSerializer
)

class CategoryListView(generics.ListAPIView):
    """
    Kategorileri MPTT sırasına göre listeler.
    Her kategorinin altındaki ürünleri de içerir.
    """
    serializer_class = CategoryWithProductsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category_type', 'level']
    search_fields = ['title_tr', 'title_en', 'description_tr', 'description_en']
    ordering_fields = ['lft', 'level', 'id']
    ordering = ['lft']  # MPTT left değerine göre sırala
    
    def get_queryset(self):
        """Sadece root kategorileri getir (level=0)"""
        return Item.objects.filter(
            item_type='category',
            level=0  # Sadece ana kategoriler
        ).prefetch_related('children')
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Dil kodu (tr/en)',
                enum=['tr', 'en']
            ),
            OpenApiParameter(
                name='category_type',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Kategori tipi',
                enum=['type1', 'type2', 'type3', 'type4']
            ),
        ],
        responses={200: CategoryWithProductsSerializer(many=True)},
        description="Kategorileri ve alt ürünlerini MPTT sırasına göre listeler"
    )
    def get(self, request, *args, **kwargs):
        # Dil ayarını kontrol et
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        
        return super().get(request, *args, **kwargs)

class ProductListView(generics.ListAPIView):
    """
    Tüm ürünleri listeler
    """
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title_tr', 'title_en', 'description_tr', 'description_en']
    ordering_fields = ['id', 'lft']
    ordering = ['lft']
    
    def get_queryset(self):
        return Item.objects.filter(item_type='product').select_related('parent')
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Dil kodu (tr/en)',
                enum=['tr', 'en']
            ),
            OpenApiParameter(
                name='category',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Kategori ID filtresi'
            ),
        ],
        responses={200: ProductSerializer(many=True)},
        description="Ürünleri listeler"
    )
    def get(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        
        return super().get(request, *args, **kwargs)

class SliderListView(generics.ListAPIView):
    """
    Slider öğelerini listeler
    """
    serializer_class = SliderSerializer
    ordering = ['lft']
    
    def get_queryset(self):
        # Slider modelini kullan
        from .models import Slider  # Import ekle
        return Slider.objects.all()
    
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
        responses={200: SliderSerializer(many=True)},
        description="Slider öğelerini listeler"
    )
    def get(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        
        return super().get(request, *args, **kwargs)