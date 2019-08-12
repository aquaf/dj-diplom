from django.shortcuts import render, redirect
from .models import Cart, Order
from products.models import Product
# Create your views here.

def cart_view(request):
    template = 'cart/cart.html'

    cart_obj = Cart.objects.new_or_get(request)
    return render(request, template, {'cart': cart_obj})

def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect(cart_view)
        cart_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
    return redirect(cart_view)

def cart_success(request):
    template = 'cart/success.html'

    if request.POST.get('success'):
        user = request.user
        cart_obj = Cart.objects.new_or_get(request)
        cart_obj.purchased = True
        order = Order.objects.create(user=user, total=cart_obj.total)
        for product in cart_obj.products.all():
            order.products.add(product)
        cart_obj.save()
        return render(request, template, {'user': request.user})
