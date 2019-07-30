from django.contrib import admin
from .models import Category, Product, Review, Blog

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'parent', 'visible',)
    list_display = ('title', 'slug', 'parent', 'visible')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ('image', 'title', 'description', 'price', 'slug', 'category',)
    list_display = ('title', 'price','category', 'slug',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = ('product', 'author', 'text', 'stars', )
    list_display = ('product', 'author')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    fields = ('text', 'product', 'main_page',)
