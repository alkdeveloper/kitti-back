# products/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.core.exceptions import ValidationError

# ------------------------
# Ana Model (Category + Product birleşik)
# ------------------------
class Item(MPTTModel):
    TYPE_CHOICES = [
        ('category', _('Category')),
        ('product', _('Product')),
    ]
    
    CATEGORY_TYPE_CHOICES = [
        ('type1', _('Type 1')),
        ('type2', _('Type 2')),
        ('type3', _('Type 3')),
        ('type4', _('Type 4')),
    ]
    
    # Temel alanlar
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='item_icons/', blank=True, null=True)
    item_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='category')
    
    # Category özel alanları
    category_type = models.CharField(
        max_length=50, 
        choices=CATEGORY_TYPE_CHOICES, 
        blank=True, 
        null=True,
        help_text=_('Only for categories')
    )
    
    # MPTT alanı
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    
    class MPTTMeta:
        order_insertion_by = ['title']
    
    def clean(self):
        """Validasyon kuralları"""
        super().clean()
        
        # Sadece kaydedilmiş objeler için children kontrolü yap
        if self.pk:  # Eğer primary key varsa (yani daha önce kaydedilmişse)
            # Product'ın çocuğu olamaz
            if self.item_type == 'product' and self.children.exists():
                raise ValidationError(_('Products cannot have children'))
        
        # Category'nin sadece 1 seviye çocuğu olabilir
        if self.parent and self.parent.item_type == 'category' and self.parent.level >= 1:
            raise ValidationError(_('Categories can only have 1 level of children'))
        
        # Product'ın parent'ı sadece category olabilir
        if self.item_type == 'product' and self.parent and self.parent.item_type != 'category':
            raise ValidationError(_('Product parent must be a category'))
        
        # Category type sadece category için
        if self.item_type != 'category' and self.category_type:
            raise ValidationError(_('Category type can only be set for categories'))
    
    def save(self, *args, **kwargs):
        # İlk kayıtta children kontrolü yapmadan kaydet
        if not self.pk:
            super().save(*args, **kwargs)
        else:
            # Güncellemede full validation yap
            self.clean()
            super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_item_type_display()}: {self.title}"
    
    @property
    def is_category(self):
        return self.item_type == 'category'
    
    @property
    def is_product(self):
        return self.item_type == 'product'


# ------------------------
# Product Image Modeli
# ------------------------
class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='item_images/')
    
    def __str__(self):
        return f"Image for {self.item.title}"

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
