from django.contrib import admin
from .models import Restaurant, Branch, Menu, MenuItem

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1

class BranchInline(admin.TabularInline):
    model = Branch
    extra = 1
    fields = ['branch_name', 'address', 'contact_number', 'owners']

class RestaurantAdmin(admin.ModelAdmin):
    inlines = [BranchInline]
    filter_horizontal = ("owners",)

class BranchAdmin(admin.ModelAdmin):
    list_display = ('branch_name', 'address', 'contact_number', 'restaurant')
    search_fields = ('branch_name', 'address')
    filter_horizontal = ('owners',)

class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'description')
    list_filter = ('branch',)
    search_fields = ('name', 'description')
    inlines = [MenuItemInline] 

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu', 'description', 'price')
    list_filter = ('menu',)
    search_fields = ('name', 'description')

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)