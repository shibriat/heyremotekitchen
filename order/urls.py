from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
from .views import OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')

urlpatterns = [
    # Regular views
    path("get-orders/", views.get_orders, name='get_orders'),
    path("", views.order_view, name='order_list'),
    path("<int:pk>/", views.order_detail_view, name='order_detail'),
    path("create/", views.create_order, name='create_order'),
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    
    # API views
    path("api/", include(router.urls)),
]