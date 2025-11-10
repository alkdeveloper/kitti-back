# products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryListView, 
    ProductListView, 
    ProductViewSet,
    CategoryViewSet,
    SliderListView,
    SliderViewSet,
)

router = DefaultRouter()
router.register('items', ProductViewSet, basename='product-items')
router.register('categories', CategoryViewSet, basename='category-items')
router.register('sliders', SliderViewSet, basename='slider-items')

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    # SliderListView kaldırıldı, router üzerinden SliderViewSet kullanılıyor
    path('', include(router.urls)),
]