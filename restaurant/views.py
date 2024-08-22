from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Branch, Menu
from django.contrib.auth.decorators import login_required

@login_required
def restaurant_list(request):
    restaurants = Restaurant.objects.filter(owners=request.user)
    return render(request, "restaurant/restaurant_list.html", {"restaurants": restaurants})

@login_required
def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk, owners=request.user)
    branches = restaurant.branches.all()
    return render(request, "restaurant/restaurant_detail.html", {"restaurant": restaurant, "branches": branches})

@login_required
def branch_detail(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    if request.user not in branch.owners.all() and request.user not in branch.restaurant.owners.all():
        return redirect('restaurant_list')
    menus = branch.menus.all()
    return render(request, "restaurant/branch_detail.html", {"branch": branch, "menus": menus})

@login_required
def menu_list(request, branch_pk):
    branch = get_object_or_404(Branch, pk=branch_pk)
    if request.user not in branch.owners.all() and request.user not in branch.restaurant.owners.all():
        return redirect('restaurant_list')
    menus = branch.menus.all()
    return render(request, "restaurant/menu_list.html", {"branch": branch, "menus": menus})