from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from restaurant.models import MenuItem
from .models import Order, OrderItem
from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer, OrderItemSerializer
from .permissions import IsOrderOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OrderSerializer
import json


@login_required
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


@login_required
def order_view(request):
    return render(request, 'order/order_list.html')


@login_required
def order_detail_view(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    order = get_object_or_404(Order, pk=pk)

    if not request.user.is_superuser and order.user != request.user:
        return JsonResponse({"error": "Forbidden"}, status=403)

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


def create_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))

            branch_id = data.get('branch_id')
            items = data.get('items', [])
            total_price = float(data.get('total_price', 0))

            if not branch_id:
                return JsonResponse({'error': 'Branch ID is required'}, status=400)

            order = Order.objects.create(
                user=request.user, branch_id=branch_id, total_price=total_price)

            for item in items:
                menu_item_name = item['menu_item']
                quantity = int(item['quantity'])
                price = float(item['price'])
                total_price_item = float(item['total_price'])

                menu_item = MenuItem.objects.get(name=menu_item_name)
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=quantity,
                    price=price
                )

            order.calculate_total()

            return JsonResponse({'message': 'Order created successfully!'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except MenuItem.DoesNotExist:
            return JsonResponse({'error': 'Menu item not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


# API
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(user=user)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]


class GetOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        branch_id = request.GET.get('branch')

        orders = Order.objects.all()
        if branch_id:
            orders = orders.filter(branch_id=branch_id)

        serializer = OrderSerializer(orders, many=True)
        return Response({"orders": serializer.data})


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order)
        return Response({"order": serializer.data})


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
