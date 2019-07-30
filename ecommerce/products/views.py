from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, FormView, View
from django.views.generic.edit import ModelFormMixin
from .models import Product, Category, Review, Blog
from django.http import Http404
from cart.models import Cart
from .forms import ReviewForm

# Create your views here.


class CategoryListView(ListView):
    template_name = "products/category.html"
    paginate_by = 4

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=self.category)
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        cart_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        context['category'] = self.category
        return context


class ProductDetailView(ModelFormMixin, DetailView):
    template_name = "products/product.html"
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context =  super(ProductDetailView, self).get_context_data(**kwargs)
        cart_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        comments = Review.objects.filter(product=self.get_object())
        context['comments'] = comments
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        form = self.get_form()
        if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.product = product
                if request.user.is_authenticated:
                    new_comment.author = request.user
                    new_comment.save()
                else:
                    new_comment.author = None
                    new_comment.save()
                return redirect(product)
            
    def get_object(self):
        product_slug = self.kwargs.get('product_slug')
        return get_object_or_404(Product, slug=product_slug)

class HomeView(View):

    def get(self, request, *args, **kwargs):
        template_name = "products/index.html"
        posts = Blog.objects.filter(main_page=True)
        cart_obj = Cart.objects.new_or_get(request)
        return render(request, template_name, context = {'posts': posts, 'cart': cart_obj})