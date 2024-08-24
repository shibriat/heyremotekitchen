from django.db import models
from django.contrib.auth.models import User
from restaurant.models import MenuItem, Branch
from decimal import Decimal


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders")
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ], default='pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def calculate_total(self):
        total = sum(Decimal(item.get_total_price())
                    for item in self.items.all())
        if self.discount > Decimal('0.00'):
            total -= total * (self.discount / Decimal('100.00'))
        self.total_price = total
        self.save()
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

    def get_total_price(self):
        return self.price * self.quantity
