from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.forms import ModelForm

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
        verbose_name = 'Редактирование разделов'
        verbose_name_plural = 'Редактирование разделов'

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
        verbose_name = 'Редактирование товаров'
        verbose_name_plural = 'Редактирование товаров'

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('product', kwargs={'category_slug': self.category.slug, 'product_slug': self.slug})


class Review(models.Model):
    REVIEW_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField()
    stars = models.IntegerField(choices=REVIEW_CHOICES, verbose_name='Количество звезд')
    timestamp = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    

    def __str__(self):
        return self.text


class Blog(models.Model):
    text = models.TextField()
    product = models.ManyToManyField(Product, blank=True)
    main_page = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = 'Редактирование статей на главной странице.'
        verbose_name_plural = 'Редактирование статей на главной странице.'