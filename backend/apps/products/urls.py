from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import ProductViewSet, ProductCategoryViewSet

router = DefaultRouter()
router.register(r'items', ProductViewSet, basename='product')
router.register(r'categories', ProductCategoryViewSet, basename='product-category')


urlpatterns = [
    path('statistics/', views.SellStatisticView.as_view())
]

urlpatterns += router.urls
