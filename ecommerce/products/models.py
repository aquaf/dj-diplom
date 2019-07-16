from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    MENU_VISIBLE_CHOICES = [
        ('d-none', 'invisible'),
        (' ', 'visible')
    ]
    
    title = models.CharField(max_length=200, verbose_name='Категория')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')
    visible = models.CharField(choices=MENU_VISIBLE_CHOICES, default='visible', max_length=15, verbose_name='Видимость')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.PROTECT, verbose_name='Родительская категория')

    class Meta:
        unique_together = ('slug', 'parent',) 
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Товар')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(decimal_places=2, max_digits=20, default=None, verbose_name='Цена')
    image = models.ImageField(null=True, blank=True, upload_to=f'images/%Y/%m/%d', verbose_name='Изображение')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category', verbose_name='Категория')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('product', kwargs={'category_slug': self.category.slug, 'product_slug': self.slug})


# class Comment(models.Model):
#     post = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')
#     author = models.CharField(max_length=200)
#     text = models.TextField()
#     created_date = models.DateTimeField(default=timezone.now)
#     approved_comment = models.BooleanField(default=False)

#     def approve(self):
#         self.approved_comment = True
#         self.save()

#     def __str__(self):
#         return self.text