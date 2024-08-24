from django.shortcuts import render
from django.utils import timezone
from order.models import Order
from restaurant.models import Branch, Menu, MenuItem 
from django.db.models import Sum
from django.contrib.auth.models import User


def dashboard_view(request):

    today = timezone.now().date()

    orders_today = Order.objects.filter(
        user=request.user, created_at__date=today).count()
    total_amount_orders_today = Order.objects.filter(user=request.user, created_at__date=today).aggregate(
        total_amount=Sum('total_price'))['total_amount'] or 0

    owned_branches = Branch.objects.filter(owners=request.user)
    owned_menus = Menu.objects.filter(branch__in=owned_branches)
    total_menu_items = MenuItem.objects.filter(menu__in=owned_menus).count()

    total_users = User.objects.count()

    context = {
        "total_users": total_users,
        "orders_today": orders_today,
        "total_amount_orders_today": total_amount_orders_today,
        "total_menu_items": total_menu_items
    }

    return render(request, "home/home.html", context)
