from rest_framework.routers import DefaultRouter

from api import views

app_name = 'api'

router = DefaultRouter()
router.register('products', views.ProductViewSet,basename='products')
router.register('payment', views.PaymentViewSet,basename='payment')
router.register('order', views.OrderViewSet,basename='order')

urlpatterns = router.urls
