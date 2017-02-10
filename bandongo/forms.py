from django import forms
from models import Member, Catalog

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('name','phone','remark','saving')

class PicForm(forms.Form):
    homePic = forms.ImageField(label='Home Picture', widget=forms.FileInput(attrs={'class': 'filestyle'}))

class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ['foodShop', 'name', 'pic', 'price']






