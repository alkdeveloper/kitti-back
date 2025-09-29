# products/urls.py
from django.urls import path
from .views import (
    CategoryListView, 
    ProductListView, 
    SliderListView,
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('sliders/', SliderListView.as_view(), name='slider-list'),
]