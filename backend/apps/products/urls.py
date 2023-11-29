from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import ProductViewSet


router = DefaultRouter()
router.register(r'', ProductViewSet, basename='product')


urlpatterns = [
    path('statistics/', views.SellStatisticView.as_view())
]

urlpatterns += router.urls
