from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'branch', 'created_at', 'total_price', 'status')
    list_filter = ('status', 'created_at', 'branch')
    search_fields = ('user__username', 'branch__branch_name')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'price')
    search_fields = ('order__id', 'menu_item__name')
    list_filter = ('order__status', 'menu_item__menu__branch__branch_name')