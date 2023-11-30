from rest_framework.routers import DefaultRouter
from .views import OrderViewSet


router = DefaultRouter()
router.register(r'', OrderViewSet, basename='order')

urlpatterns = [
    # ... other urlpatterns ...
]

urlpatterns += router.urls
