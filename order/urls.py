from django.urls import path
from . import views

urlpatterns = [
    path("get-orders/", views.get_orders, name='get_orders'),
    path("", views.order_view, name='order_list'),
    path("<int:pk>/", views.order_detail_view, name='order_detail'),
]