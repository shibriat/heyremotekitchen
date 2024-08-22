from django.contrib.auth.models import User
from django.db import models
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    can_add_restaurant = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username