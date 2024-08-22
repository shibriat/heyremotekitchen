from django.urls import path
from . import views

urlpatterns = [
    path("", views.restaurant_list, name="restaurant_list"),
    path("<int:pk>/", views.restaurant_detail, name="restaurant_detail"),
    path("branch/<int:pk>/", views.branch_detail, name="branch_detail"),
    path("branch/<int:branch_pk>/menus/", views.menu_list, name="menu_list"),
]
