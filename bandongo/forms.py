from django import forms
from models import Member, Shop, Catalog, Orderlog, Savelog

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('name','member_phone','member_mark','member_saving')










