from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Order


def get_orders(request):
    branch_id = request.GET.get('branch')

    orders = Order.objects.all()
    if branch_id:
        orders = orders.filter(branch_id=branch_id)

    orders_data = []
    for order in orders:
        orders_data.append({
            "id": order.id,
            "user": order.user.username,
            "created_at": order.created_at.strftime('%Y-%m-%d %H:%M'),
            "total_price": order.total_price,
            "discount": order.discount,
            "status": order.status,
        })

    return JsonResponse({"orders": orders_data})


def order_view(request):
    return render(request, 'order/order_list.html')


def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_data = {
        "id": order.id,
        "user": order.user.username,
        "created_at": order.created_at.strftime('%Y-%m-%d %H:%M'),
        "total_price": order.total_price,
        "discount": order.discount,
        "status": order.status,
        "items": [
            {
                "menu_item": item.menu_item.name,
                "quantity": item.quantity,
                "price": item.price,
            } for item in order.items.all()
        ]
    }
    return JsonResponse({"order": order_data})
