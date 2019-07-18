from django.contrib import admin
from django.urls import path
from .views import logout_view, login_view, signup

urlpatterns = [
    path('signup/', signup, name='signup_view'),
    path('logout/', logout_view, name='logout_view'),
    path('login/', login_view, name='login_view'),
]