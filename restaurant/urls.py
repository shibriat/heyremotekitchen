from django.urls import path
from . import views

urlpatterns = [
    path("", views.restaurant_list, name="restaurant_list"),
    path("<int:pk>/", views.restaurant_detail, name="restaurant_detail"),
    path("get-restaurant/", views.get_restaurant, name="get_restaurant"),
    path("branch/", views.branch_list, name="branch_list"),
    path("get-branch/", views.get_branch, name="get_branch"),
    path("branch/<int:branch_id>/", views.get_branch, name='get_branch'),
    path("branch/update/", views.update_branch, name='update_branch'),
    path("branch/<int:branch_pk>/menus/", views.menu_list, name="menu_list"),
    path("menus/", views.menu_list, name='menu_list'),
    path("get-menu/", views.get_menu, name='get_menu'),
    path('menu-items/<int:menu_id>/', views.menu_items_list, name='menu_items_list'),
    path('update-menu-item/', views.update_menu_item, name='update_menu_item'),
    path('menu-item/<int:menu_item_id>/delete/', views.delete_menu_item, name='delete_menu_item'),
    path('menu-item/add/', views.add_menu_item, name='add_menu_item'),
    path('menu/add/', views.add_menu, name='add_menu'),
]
