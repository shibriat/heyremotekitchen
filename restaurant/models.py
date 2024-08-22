from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    owners = models.ManyToManyField(User, related_name="owned_restaurants")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Branch(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="branches")
    branch_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    owners = models.ManyToManyField(User, related_name="owned_branches")

    def __str__(self):
        return f"{self.branch_name} - {self.restaurant.name}"

class Menu(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="menus")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.branch.branch_name}"