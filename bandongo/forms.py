from django import forms
from models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('name','phone','remark','saving')

class PicForm(forms.Form):
    homePic = forms.ImageField(label='Home Picture')

# class CatalogForm(forms.ModelForm):
#     class Meta:
#         model = Catalog
        






