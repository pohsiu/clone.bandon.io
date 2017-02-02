from django.shortcuts import render, get_object_or_404
from models import Member, Shop, Catalog, Orderlog, Savelog, Beverage, Schedule
from models import Category

from .forms import MemberForm
from django.shortcuts import render_to_response, RequestContext

from django.http import HttpResponse

from django.core.urlresolvers import reverse
from django.shortcuts import redirect


from models import VehicleBrand,VehicleModel
from django.core import serializers

from datetime import datetime
from datetime import date #detail index used
from django.utils.dateparse import parse_datetime


def member_new(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            # member.name = request.user
            member.save()
            return redirect('bandongo.views.member_detail', pk=member.pk)
    else:
        form = MemberForm()
    return render(request, 'bandongo/member_edit.html', {'form': form})

def memberList(request):
    members=Member.objects.all()
    return render(request, 'bandongo/member_list.html',{'members':members})
    
def member_detail(request, pk):
    de_member = get_object_or_404(Member, pk=pk)
    return render(request, 'bandongo/member_detail.html', {'de_member': de_member})

# Create your views here.
# def userList(request):
#     users=User.objects.all()
#     return render(request, 'bandongo/user_list.html', {'users':users})



def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            # member.author = request.user
            member.save()
            return redirect('bandongo.views.member_detail', pk=member.pk)
    else:
        form = MemberForm(instance=member)
    return render(request, 'bandongo/member_edit.html', {'form': form})



##related selection example
def all_json_models(request, brand):
    current_brand = VehicleBrand.objects.get(code=brand)
    models = VehicleModel.objects.all().filter(brand=current_brand)
    json_models = serializers.serialize("json", models)
    return HttpResponse(json_models, content_type='application/json')
    
def brand_model_select(request):
    brand_list = VehicleBrand.objects.all()
    return render(request, 'bandongo/brand_model_select.html',{'brand_list' : brand_list})


#related test
def filter_json(request, mark):
    
    models = Member.objects.all().filter(member_mark=mark)
    json_models = serializers.serialize("json", models)
    return HttpResponse(json_models, content_type='application/json')
    
def mark_select(request):
    if request.method == "POST":
        member_pk = request.POST['member_name']
        return redirect('bandongo.views.mark_detail', pk=member_pk)
    
    mark_list = Member.objects.values_list('member_mark',flat=True).distinct()
    return render(request, 'bandongo/mark_select.html',{'mark_list' : mark_list})
    

def mark_detail(request, pk):
    de_member = get_object_or_404(Member, pk=pk)
#order index 

    #===get today's schedule part===
    
    today = date.today()
    schedules = Schedule.objects.filter(date=today).values_list('food','beverage')
    id_food = schedules[0][0]
    id_beverage = schedules[0][1]
    #===  part end ===
    
    #===get food catalog===
    list_food = Catalog.objects.filter(shop_name=id_food)
    #===catalog part end===
    
    #===get beverage catalog===
    # list_beverage = Catalog.objects.filter(shop_name=id_beverage).values_list('name','price')
    #===beverage part end===



    return render(request, 'bandongo/mark_detail.html', {'de_member': de_member,'list_food':list_food})

def mark2(request):
    # mark_list = Member.objects.all()
    # mark_list = serializers.serialize("json", mark_list)
    mark_list = Member.objects.values_list('member_mark',flat=True).distinct()
    return render(request, 'bandongo/mark_select_v2.html',{'mark_list':mark_list})




## backend_part
def setSchedule(request):
    shops=Shop.objects.all()
    drinks=Beverage.objects.all()
    return render(request, 'bandongo/backend_setSchedule.html',{'shops':shops, 'drinks':drinks})

def editSchedule(request):
    shops=Shop.objects.all()
    drinks=Beverage.objects.all()
    return render(request, 'bandongo/backend_editSchedule.html',{'shops':shops, 'drinks':drinks})
    
def setBandon(request):
    dueDatetime=parse_datetime(request.POST["dueDatetime"])
    nonExpire=Schedule.objects.filter(expire=False)
    bandon=Shop.objects.get(name=request.POST["bandon"])
    drink=Beverage.objects.get(name=request.POST["drink"])
    if len(nonExpire)>1:
        return HttpResponse("Server Error")
    elif len(nonExpire)==0:
        Schedule.objects.create(food=bandon, beverage=drink, date=dueDatetime)
        return HttpResponse("Registered Bandon Successfully")
    else:
        if(nonExpire[0].date<datetime.now()):
            nonExpire[0].expire=True
            nonExpire[0].save()
            Schedule.objects.create(food=bandon, beverage=drink, date=dueDatetime)
            return HttpResponse("Registered Bandon Successfully")
        else:
            return HttpResponse("Another schedule has not expired.")