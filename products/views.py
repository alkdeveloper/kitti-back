# products/views.py
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.utils.translation import activate
from .models import Item, ItemImage, Slider
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    CategoryWithProductsSerializer,
    CategoryProductsSerializer,
    SliderSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Kategorileri yönetmek için CRUD işlemleri
    """
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category_type', 'level']
    search_fields = ['title_tr', 'title_en', 'description_tr', 'description_en']
    ordering_fields = ['lft', 'level', 'id']
    ordering = ['lft']
    
    def get_queryset(self):
        """Sadece kategorileri getir"""
        return Item.objects.filter(item_type='category').prefetch_related('children')
    
    @extend_schema(
        summary="Kategorileri Listele",
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
                enum=['type1', 'type2', 'type3', 'type4', 'type5']
            ),
        ],
        responses={200: CategorySerializer(many=True)},
        description="Kategorileri listeler"
    )
    def list(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Kategori Oluştur",
        parameters=[
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Dil kodu (tr/en)',
                enum=['tr', 'en']
            ),
        ],
        request=CategorySerializer,
        responses={201: CategorySerializer},
        description="Yeni kategori oluşturur"
    )
    def create(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Kategori Güncelle",
        parameters=[
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Dil kodu (tr/en)',
                enum=['tr', 'en']
            ),
        ],
        request=CategorySerializer,
        responses={200: CategorySerializer},
        description="Kategoriyi günceller"
    )
    def update(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Kategoriyi Kısmi Güncelle",
        parameters=[
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Dil kodu (tr/en)',
                enum=['tr', 'en']
            ),
        ],
        request=CategorySerializer,
        responses={200: CategorySerializer},
        description="Kategoriyi kısmi olarak günceller"
    )
    def partial_update(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Kategori Detayı",
        parameters=[
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Dil kodu (tr/en)',
                enum=['tr', 'en']
            ),
        ],
        responses={200: CategorySerializer},
        description="Kategori detayını getirir"
    )
    def retrieve(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        return super().retrieve(request, *args, **kwargs)

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

class ProductViewSet(viewsets.ModelViewSet):
    """
    Ürünleri yönetmek için CRUD işlemleri
    """
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title_tr', 'title_en', 'description_tr', 'description_en']
    ordering_fields = ['id', 'lft']
    ordering = ['lft']
    
    def get_queryset(self):
        queryset = Item.objects.filter(item_type='product').select_related('parent').prefetch_related('images')
        # Kategori filtresi
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(parent_id=category)
        return queryset
    
    @extend_schema(
        summary="Ürünleri Listele",
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
    def list(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Ürün Oluştur",
        parameters=[
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Dil kodu (tr/en)',
                enum=['tr', 'en']
            ),
        ],
        request=ProductSerializer,
        responses={201: ProductSerializer},
        description="Yeni ürün oluşturur"
    )
    def create(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Ürün Güncelle",
        parameters=[
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Dil kodu (tr/en)',
                enum=['tr', 'en']
            ),
        ],
        request=ProductSerializer,
        responses={200: ProductSerializer},
        description="Ürünü günceller"
    )
    def update(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Ürünü Kısmi Güncelle",
        parameters=[
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Dil kodu (tr/en)',
                enum=['tr', 'en']
            ),
        ],
        request=ProductSerializer,
        responses={200: ProductSerializer},
        description="Ürünü kısmi olarak günceller"
    )
    def partial_update(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Ürün Detayı",
        parameters=[
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Dil kodu (tr/en)',
                enum=['tr', 'en']
            ),
        ],
        responses={200: ProductSerializer},
        description="Ürün detayını getirir"
    )
    def retrieve(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        return super().retrieve(request, *args, **kwargs)

# Eski ProductListView (geriye dönük uyumluluk için)
class ProductListView(generics.ListAPIView):
    """
    Tüm ürünleri listeler (geriye dönük uyumluluk için)
    """
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title_tr', 'title_en', 'description_tr', 'description_en']
    ordering_fields = ['id', 'lft']
    ordering = ['lft']
    
    def get_queryset(self):
        queryset = Item.objects.filter(item_type='product').select_related('parent').prefetch_related('images')
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(parent_id=category)
        return queryset
    
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

class SliderViewSet(viewsets.ModelViewSet):
    """
    Slider'ları yönetmek için CRUD işlemleri
    """
    serializer_class = SliderSerializer
    permission_classes = [AllowAny]
    ordering = ['lft']
    
    def get_queryset(self):
        return Slider.objects.all()
    
    @extend_schema(
        summary="Slider'ları Listele",
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
    def list(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Slider Oluştur",
        parameters=[
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Dil kodu (tr/en)',
                enum=['tr', 'en']
            ),
        ],
        request=SliderSerializer,
        responses={201: SliderSerializer},
        description="Yeni slider oluşturur"
    )
    def create(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Slider Güncelle",
        parameters=[
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Dil kodu (tr/en)',
                enum=['tr', 'en']
            ),
        ],
        request=SliderSerializer,
        responses={200: SliderSerializer},
        description="Slider'ı günceller"
    )
    def update(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Slider'ı Kısmi Güncelle",
        parameters=[
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Dil kodu (tr/en)',
                enum=['tr', 'en']
            ),
        ],
        request=SliderSerializer,
        responses={200: SliderSerializer},
        description="Slider'ı kısmi olarak günceller"
    )
    def partial_update(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Slider Detayı",
        parameters=[
            OpenApiParameter(
                name='lang',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Dil kodu (tr/en)',
                enum=['tr', 'en']
            ),
        ],
        responses={200: SliderSerializer},
        description="Slider detayını getirir"
    )
    def retrieve(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        return super().retrieve(request, *args, **kwargs)

# Eski SliderListView (geriye dönük uyumluluk için)
class SliderListView(generics.ListAPIView):
    """
    Slider öğelerini listeler (geriye dönük uyumluluk için)
    """
    serializer_class = SliderSerializer
    ordering = ['lft']
    
    def get_queryset(self):
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

class CategoriesWithProductsView(generics.ListAPIView):
    """
    Tüm kategorileri ve her kategorinin altındaki ürünleri döndürür.
    JSON formatında nested yapı: categories -> products
    """
    serializer_class = CategoryProductsSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category_type', 'level']
    search_fields = ['title_tr', 'title_en', 'description_tr', 'description_en']
    ordering_fields = ['lft', 'level', 'id']
    ordering = ['lft']
    
    def get_queryset(self):
        """Sadece kategorileri getir (parent=None olanlar veya tüm kategoriler)"""
        queryset = Item.objects.filter(item_type='category').prefetch_related('children', 'children__images')
        
        # Eğer sadece root kategorileri istiyorsa
        root_only = self.request.query_params.get('root_only', 'false').lower() == 'true'
        if root_only:
            queryset = queryset.filter(level=0)
        
        return queryset
    
    @extend_schema(
        summary="Kategoriler ve Ürünleri Listele",
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
                enum=['type1', 'type2', 'type3', 'type4', 'type5']
            ),
            OpenApiParameter(
                name='root_only',
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description='Sadece root kategorileri getir (true/false)',
            ),
        ],
        responses={200: CategoryProductsSerializer(many=True)},
        description="Tüm kategorileri ve her kategorinin altındaki ürünleri listeler"
    )
    def get(self, request, *args, **kwargs):
        # Dil ayarını kontrol et
        lang = request.query_params.get('lang', 'tr')
        if lang in ['tr', 'en']:
            activate(lang)
        
        # Response'u özelleştir
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'categories': serializer.data
        })