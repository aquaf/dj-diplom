from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Category
from django.http import Http404

# Create your views here.


class CategoryListView(ListView):
    template_name = "products/category.html"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=self.category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProductDetailView(DetailView):
    template_name = "products/product.html"
    
    def get_object(self):
        product_slug = self.kwargs.get('product_slug')
        return get_object_or_404(Product, slug=product_slug)

class HomeView(TemplateView):
    template_name = "products/index.html"