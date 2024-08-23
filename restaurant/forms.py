from django import forms
from .models import Restaurant, Branch


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'description']

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['id', 'branch_name', 'address', 'contact_number']
