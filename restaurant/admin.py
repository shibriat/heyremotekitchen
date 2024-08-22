from django.contrib import admin
from .models import Restaurant, Branch, Menu

class BranchInline(admin.TabularInline):
    model = Branch
    extra = 1

class RestaurantAdmin(admin.ModelAdmin):
    inlines = [BranchInline]
    filter_horizontal = ("owners",)

class BranchAdmin(admin.ModelAdmin):
    filter_horizontal = ("owners",)

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Menu)