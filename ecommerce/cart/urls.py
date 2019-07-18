from django.urls import path
from .views import cart_view, cart_update, cart_success

urlpatterns = [
    path('', cart_view, name='cart_view'),
    path('update/', cart_update, name='cart_update'),
    path('success/', cart_success, name='cart_success'),
]