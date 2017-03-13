from django import forms
from models import Member, Catalog, Food, Drink, Category
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('name','phone','remark','saving')

class PicForm(forms.Form):
    homePic = forms.ImageField(label='Home Picture', widget=forms.ClearableFileInput(attrs={'class': 'filestyle'}))

class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ['foodShop', 'name', 'pic', 'price']
        widgets = {
            'foodShop': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'pic': forms.ClearableFileInput(attrs={'class': 'filestyle'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'pic', 'telephone', 'address', 'remark']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'pic': forms.ClearableFileInput(attrs={'class': 'filestyle'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'remark': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DrinkForm(forms.ModelForm):
    class Meta:
        model = Drink
        fields = ['name', 'pic', 'telephone', 'address', 'remark']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'pic': forms.ClearableFileInput(attrs={'class': 'filestyle'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'remark': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'bag']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'bag': forms.NumberInput(attrs={'class': 'form-control'}),
        }




