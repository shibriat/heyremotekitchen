from django.shortcuts import render
from django.contrib.auth.models import User

def dashboard_view(request):
    total_users = User.objects.count()  
    return render(request, "home/home.html", {"total_users": total_users})