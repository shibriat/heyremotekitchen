from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from restaurant.models import Restaurant, Branch, Menu, MenuItem
from order.models import Order

class Command(BaseCommand):
    help = 'Populate the database with multiple restaurants, branches, menus, and menu items'

    def handle(self, *args, **options):
        # Create superuser
        superuser = User.objects.create_superuser(
            username='superuser',
            email='superuser@example.com',
            password='superpassword'
        )
        self.stdout.write(self.style.SUCCESS('Superuser created'))

        # Create regular users
        users = [
            User.objects.create_user(username='user1', email='user1@example.com', password='userpassword1'),
            User.objects.create_user(username='user2', email='user2@example.com', password='userpassword2'),
            User.objects.create_user(username='user3', email='user3@example.com', password='userpassword3'),
        ]
        self.stdout.write(self.style.SUCCESS('Regular users created'))

        # Create sample restaurants
        restaurants = [
            Restaurant.objects.create(name='Restaurant A', description='Description for Restaurant A'),
            Restaurant.objects.create(name='Restaurant B', description='Description for Restaurant B'),
            Restaurant.objects.create(name='Restaurant C', description='Description for Restaurant C'),
        ]
        self.stdout.write(self.style.SUCCESS('Restaurants created'))

        # Create sample branches
        branches = [
            Branch.objects.create(restaurant=restaurants[0], branch_name='Main Branch A', address='123 Main St, City A', contact_number='111111111'),
            Branch.objects.create(restaurant=restaurants[0], branch_name='Secondary Branch A', address='124 Main St, City A', contact_number='111111112'),
            Branch.objects.create(restaurant=restaurants[1], branch_name='Main Branch B', address='456 Main St, City B', contact_number='222222222'),
            Branch.objects.create(restaurant=restaurants[1], branch_name='Secondary Branch B', address='457 Main St, City B', contact_number='222222223'),
            Branch.objects.create(restaurant=restaurants[2], branch_name='Main Branch C', address='789 Main St, City C', contact_number='333333333'),
        ]
        self.stdout.write(self.style.SUCCESS('Branches created'))

        # Assign users as owners
        for i, restaurant in enumerate(restaurants):
            restaurant.owners.add(users[i % len(users)])
            for branch in branches:
                if branch.restaurant == restaurant:
                    branch.owners.add(users[i % len(users)])
        self.stdout.write(self.style.SUCCESS('Users assigned as owners'))

        # Create sample menus and menu items
        menu_items = []
        for branch in branches:
            for i in range(1, 3):  # Two menus per branch
                menu = Menu.objects.create(branch=branch, name=f'Menu {i} for {branch.branch_name}', description=f'Description for Menu {i}')
                self.stdout.write(self.style.SUCCESS(f'Menu {i} created for {branch.branch_name}'))
                for j in range(1, 4):  # Three items per menu
                    item = MenuItem.objects.create(
                        menu=menu,
                        name=f'MenuItem {j} for {menu.name}',
                        description=f'Description for MenuItem {j}',
                        price=10.00 + j
                    )
                    menu_items.append(item)
                    self.stdout.write(self.style.SUCCESS(f'MenuItem {j} created for {menu.name}'))

        # Create sample orders
        for user in users:
            for branch in branches:
                order = Order.objects.create(
                    user=user,
                    branch=branch,
                    total_price=0.00,
                    discount=5.00,
                    status='pending'
                )
                for item in menu_items[:3]:  # Use only the first 3 items for simplicity
                    order.items.create(
                        menu_item=item,
                        quantity=1,
                        price=item.price
                    )
                order.calculate_total()
                self.stdout.write(self.style.SUCCESS(f'Order created for {user.username} at {branch.branch_name}'))