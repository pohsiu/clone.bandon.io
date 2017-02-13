from django import forms
from models import Member, Catalog

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






