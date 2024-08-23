from django.shortcuts import render, get_object_or_404, redirect
from .models import MenuItem, Restaurant, Branch, Menu
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import RestaurantForm, BranchForm
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token


@login_required
def restaurant_list(request):
    if request.method == 'POST':
        if not request.user.profile.can_add_restaurant:
            return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)

        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.save()
            restaurant.owners.add(request.user)
            return JsonResponse({'success': True})

    restaurants = Restaurant.objects.filter(owners=request.user)
    return render(request, "restaurant/restaurant_list.html", {"restaurants": restaurants})


@login_required
def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)

    if not restaurant.owners.filter(id=request.user.id).exists():
        return JsonResponse({'error': 'You do not have permission to view this restaurant.'}, status=403)

    branches = restaurant.branches.all().values(
        'id', 'branch_name', 'address', 'contact_number')

    response_data = {
        'name': restaurant.name,
        'description': restaurant.description,
        'branches': list(branches)
    }

    return JsonResponse(response_data)


@login_required
def get_restaurant(request):
    restaurants = Restaurant.objects.filter(
        owners=request.user).values('id', 'name')

    return JsonResponse({'restaurants': list(restaurants)})


@login_required
def get_branch(request):
    restaurant_id = request.GET.get('restaurant_id')
    branches = []
    if restaurant_id:
        branches = Branch.objects.filter(restaurant_id=restaurant_id).values(
            'id', 'branch_name', 'address', 'contact_number'
        )

    return JsonResponse({
        'branches': list(branches)
    })


@login_required
def branch_list(request):
    return render(request, "restaurant/branch_list.html")


@login_required
def update_branch(request):
    if request.method == 'POST':
        branch_id = request.POST.get('branch_id')
        branch_name = request.POST.get('branch_name')
        address = request.POST.get('address')
        contact_number = request.POST.get('contact_number')

        branch = get_object_or_404(Branch, id=branch_id)

        # Update the branch fields
        branch.branch_name = branch_name
        branch.address = address
        branch.contact_number = contact_number
        branch.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def menu_list(request):
    return render(request, "restaurant/menu_list.html")


@login_required
def get_menu(request):
    branch_id = request.GET.get('branch_id')
    if branch_id:
        branch = Branch.objects.filter(
            id=branch_id, owners=request.user).first()
        if not branch:
            return JsonResponse({'error': 'You do not have permission to view this branch.'}, status=403)

        menus = Menu.objects.filter(branch=branch).values(
            'id', 'name', 'description')
        return JsonResponse({'menus': list(menus)})
    return JsonResponse({'error': 'Branch ID not provided'}, status=400)


@login_required
def menu_items_list(request, menu_id):
    try:
        menu = Menu.objects.get(id=menu_id, branch__owners=request.user)
    except Menu.DoesNotExist:
        return JsonResponse({'error': 'You do not have permission to view this menu.'}, status=403)

    menu_items = MenuItem.objects.filter(menu=menu).values(
        'id', 'name', 'description', 'price'
    )
    return JsonResponse({'menu_items': list(menu_items)})


@csrf_protect
@require_POST
def update_menu_item(request):
    try:
        item_id = request.POST.get('id')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        menu_item = MenuItem.objects.get(id=item_id)

        menu_item.name = name
        menu_item.description = description
        menu_item.price = price
        menu_item.save()

        return JsonResponse({'status': 'success'}, status=200)

    except MenuItem.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Menu item not found'}, status=404)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_protect
@require_POST
def delete_menu_item(request, menu_item_id):
    try:
        menu_item = MenuItem.objects.get(id=menu_item_id)
        menu_item.delete()
        return JsonResponse({'status': 'success'})
    except MenuItem.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Menu item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@require_POST
def add_menu_item(request):
    try:
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        menu_id = request.POST.get('menu_id')

        MenuItem.objects.create(
            name=name, description=description, price=price, menu_id=menu_id)

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
@require_POST
def add_menu(request):
    name = request.POST.get('name')
    description = request.POST.get('description')
    branch_id = request.POST.get('branch_id')

    if not name or not branch_id:
        return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

    try:
        branch = Branch.objects.get(id=branch_id)
        menu = Menu.objects.create(
            branch=branch, name=name, description=description)
        return JsonResponse({'status': 'success', 'menu_id': menu.id})
    except Branch.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Branch does not exist'}, status=404)
