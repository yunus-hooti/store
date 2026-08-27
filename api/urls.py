from rest_framework.routers import DefaultRouter

from api import views

app_name = 'api'

router = DefaultRouter()
router.register('products', views.ProductViewSet,basename='products')

urlpatterns = router.urls
