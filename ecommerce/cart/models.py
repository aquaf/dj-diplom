from django.db import models
from django.conf import settings
from django.urls import reverse
from products.models import Product
from django.db.models.signals import pre_save, post_save, m2m_changed

# Create your models here.

class CartManager(models.Manager):
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        cart_obj = self.get_queryset().filter(id=cart_id).first()
        if cart_obj:
            if cart_obj.purchased:
                cart_obj = Cart.objects.new(user=request.user)
                request.session['cart_id'] = cart_obj.id
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            request.session['cart_id'] = cart_obj.id
        return cart_obj


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    purchased = models.BooleanField(default=False)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


def m2m_changed_cart_reciever(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        instance.total = total
        instance.save()


m2m_changed.connect(m2m_changed_cart_reciever, sender=Cart.products.through)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Покупатель', null=True)
    timestamp = models.DateTimeField(verbose_name='Время заказа', auto_now_add=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    products = models.ManyToManyField(Product, verbose_name='Товар', null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.id} от {self.timestamp.date()}'

    def order_num(self):
        return f'Заказ №{self.id}'
