from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Branch, Menu
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Restaurant
from .forms import RestaurantForm


@login_required
def restaurant_list(request):
    # Check if the user has permission to add a new restaurant
    if request.method == 'POST':
        if not request.user.profile.can_add_restaurant:
            return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)

        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.save()
            restaurant.owners.add(request.user)
            return JsonResponse({'success': True})

    # Fetch the list of restaurants for the user
    restaurants = Restaurant.objects.filter(owners=request.user)
    return render(request, "restaurant/restaurant_list.html", {"restaurants": restaurants})


@login_required
def restaurant_detail(request, pk):
    try:
        restaurant = Restaurant.objects.get(pk=pk)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restaurant not found'}, status=404)

    branches = restaurant.branches.all().values(
        'id', 'branch_name', 'address', 'contact_number')

    response_data = {
        'name': restaurant.name,
        'description': restaurant.description,
        'branches': list(branches)
    }

    return JsonResponse(response_data)


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
