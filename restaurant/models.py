from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    owners = models.ManyToManyField(User, related_name="owned_restaurants")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Branch(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="branches")
    branch_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    owners = models.ManyToManyField(User, related_name="owned_branches")

    def __str__(self):
        return f"{self.branch_name} - {self.restaurant.name}"


class Employee(models.Model):
    EMPLOYEE_POSITION_CHOICES = [
        ('Manager', 'Manager'),
        ('Chef', 'Chef'),
        ('Waiter', 'Waiter'),
        ('Cashier', 'Cashier'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="employees", null=True, blank=True)
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name="employees", null=True, blank=True)
    position = models.CharField(
        max_length=50, choices=EMPLOYEE_POSITION_CHOICES)
    date_hired = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} - {self.position}"


class Menu(models.Model):
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name="menus")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.branch.branch_name}"


class MenuItem(models.Model):
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"
