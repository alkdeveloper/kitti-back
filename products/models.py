from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from modeltranslation.translator import register, TranslationOptions

# ------------------------
# Kategori Modeli
# ------------------------
class Category(MPTTModel):
    TYPE_CHOICES = [
        ('type1', _('Type 1')),
        ('type2', _('Type 2')),
        ('type3', _('Type 3')),
        ('type4', _('Type 4')),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

# ------------------------
# Ürün Modeli (MPTTModel ile sıralanabilir)
# ------------------------
class Product(MPTTModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='product_icons/', blank=True, null=True)
    category = TreeForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

# ------------------------
# Slider Modeli (MPTTModel ile sıralanabilir)
# ------------------------
class Slider(MPTTModel):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='sliders/')
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['id']

    def __str__(self):
        return self.title or f"Slider {self.id}"
