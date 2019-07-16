from django.urls import path
from .views import CategoryListView, ProductDetailView, HomeView
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<slug>/', CategoryListView.as_view(), name='category'),
    path('<category_slug>/<product_slug>/', ProductDetailView.as_view(), name='product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
