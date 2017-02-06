from django.shortcuts import render, get_object_or_404
from models import Member, Shop, Catalog, Orderlog, Savelog, Beverage, Schedule
from models import Category

from .forms import MemberForm
from django.shortcuts import render_to_response, RequestContext

from django.http import HttpResponse
from django.http import JsonResponse

from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from django.db.models import Sum


from models import VehicleBrand,VehicleModel
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

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
def filter_json(request):
    
    mark_list=Category.objects.all()
    marks = list(mark_list.values())
    # for i in range(len(marks)):
    #     marks[i]['index']=i
    models = []
    for mark in mark_list:
        models.append(list(Member.objects.all().filter(member_mark=mark).values()))
        
    return JsonResponse({'member_list': models, 'mark_list': marks})
    
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
    now = datetime.now()
    
    schedules = Schedule.objects.filter(expire=False)
    schedule_name= 'Resting'
    duedate = schedules[0].date
    if now < duedate:
        id_food = schedules[0].food
        id_beverage = schedules[0].beverage
        list_food = Catalog.objects.filter(shop_name=id_food)
        pic_beverage = Beverage.objects.filter(name=id_beverage)
        schedule_name = schedules[0].name
    else:
        list_food=''
        pic_beverage=''
        
    
    save_total = Savelog.objects.filter(member_name=pk).aggregate(save_total=Sum('money'))['save_total']
    if save_total==None:
        save_total=0
    savelogs = Savelog.objects.filter(member_name=pk).order_by('tran_date')
    
    cost_total = Orderlog.objects.filter(member_name=pk).aggregate(cost_total=Sum('orderprice'))['cost_total']
    if cost_total==None:
        cost_total=0
    costlogs = Orderlog.objects.filter(member_name=pk)
    
    total_sum = save_total - cost_total
    
    return render(request, 'bandongo/mark_detail.html', {'de_member': de_member,'list_food':list_food,'pic_beverage':pic_beverage,'save_total':save_total,'savelogs':savelogs,'cost_total':cost_total,'costlogs':costlogs,'total_sum':total_sum,'schedule_name':schedule_name})

def mark2(request):
    if request.method == "POST":
        member_pk = request.POST['member_name']
        return redirect('bandongo.views.mark_detail', pk=member_pk)
    
    mark_list = list(Category.objects.all().values())
    for i in range(len(mark_list)):
        mark_list[i]['index']=i
   
    # mark_list = Member.objects.values_list('member_mark',flat=True).distinct()
    return render(request, 'bandongo/mark_select_v2.html',{'mark_list':mark_list})




## backend_part
## page part
def setSchedulePage(request):
    shops=Shop.objects.all()
    drinks=Beverage.objects.all()
    return render(request, 'bandongo/backend_setSchedule.html',{'shops':shops, 'drinks':drinks})

def editSchedulePage(request):
    nonFinish=Schedule.objects.filter(finish=False)
    if len(nonFinish)==0:
        return render(request, 'bandongo/backend_editSchedule.html',{'nonFinish':len(nonFinish)})
    elif len(nonFinish)==1:
        shops=Shop.objects.all()
        drinks=Beverage.objects.all()
        for index in range(len(shops)):
            if shops[index]==nonFinish[0].food:
                shops[index].selected="selected"
            else:
                shops[index].selected=""
        for index in range(len(drinks)):
            if drinks[index]==nonFinish[0].beverage:
                drinks[index].selected="selected"
            else:
                drinks[index].selected=""
        
        return render(request, 'bandongo/backend_editSchedule.html',{'name': nonFinish[0].name, 'pk': nonFinish[0].pk, 'shops':shops, 'drinks':drinks, 'nonFinish': len(nonFinish), 'datetime': nonFinish[0].date.strftime("%Y-%m-%dT%H:%M")})
    else:
        print "bugbugbugbug"

def scheduleListPage(request):
    schedules=Schedule.objects.all()
    return render(request, 'bandongo/backend_scheduleList.html',{'schedules': schedules})

def orderPage(request):
    checkExpire()
    try:
        schedule=Schedule.objects.get(finish=False)
        catalogs=Catalog.objects.filter(shop_name=schedule.food)
        bags=[]
        total_price=0
        for i in range(3):
            bags.append([])
            for catalog in catalogs:
                tempOrders=Orderlog.objects.filter(schedule_name=schedule, catalog_name=catalog, member_name__member_mark__bag=(i+1))
                count=0
                price=0
                for tempOrder in tempOrders:
                    count+=tempOrder.ordernum
                    price+=tempOrder.ordernum*catalog.price
                if count > 0:
                    bags[i].append({"food_name": catalog.name, "count": count, 'price': price})
                    total_price+=price
        return render(request, 'bandongo/backend_order.html',{'schedule': schedule, 'bags': bags, 'total_price': total_price})
    except ObjectDoesNotExist:
        return render(request, 'bandongo/backend_order.html',{'schedule': None})

def orderDetailPage(request, pk):
    checkExpire()
    try:
        schedule=Schedule.objects.get(pk=pk)
        bags=[]
        for i in range(3):
            orders=Orderlog.objects.filter(schedule_name=schedule, member_name__member_mark__bag=(i+1))
            bags.append(orders)
        return render(request, 'bandongo/backend_orderDetail.html',{'schedule': schedule, 'bags': bags})
    except ObjectDoesNotExist:
        return render(request, 'bandongo/backend_orderDetail.html',{'schedule': None})

def addMemberPage(request):
    categories=Category.objects.all()
    return render(request, 'bandongo/backend_addMember.html',{'categories': categories})

## function part
def setSchedule(request):
    checkExpire()
    nonFinish=len(Schedule.objects.filter(finish=False))
    dueDatetime=parse_datetime(request.POST["dueDatetime"])
    bandon=Shop.objects.get(name=request.POST["bandon"])
    drink=Beverage.objects.get(name=request.POST["drink"])
    if nonFinish==0:
        Schedule.objects.create(name=request.POST["schedule_name"], food=bandon, beverage=drink, date=dueDatetime)
        return HttpResponse("Registered Schedule Successfully")
    else:
        return HttpResponse("Another schedule has not expired.")

def editSchedule(request):
    nonFinish=len(Schedule.objects.filter(finish=False))
    schedule=Schedule.objects.get(pk=request.POST["pk"])
    schedule.date=parse_datetime(request.POST["dueDatetime"])
    schedule.food=Shop.objects.get(name=request.POST["bandon"])
    schedule.beverage=Beverage.objects.get(name=request.POST["drink"])
    schedule.name=request.POST["schedule_name"]
    schedule.save();

    return HttpResponse("Edit Schedule Successfully")

def finishSchedule(request):
    schedule=Schedule.objects.get(pk=request.POST["pk"])
    schedule.finish=True
    schedule.save();
    return HttpResponse("Finish Schedule Successfully")

def addMember(request):
    category=Category.objects.get(category_name=request.POST["category"])
    Member.objects.create(name=request.POST["name"], member_phone=request.POST["phone"], member_email=request.POST["email"], member_mark=category)
    return HttpResponse("Add Member Successfully")

def checkExpire():
    nonExpire=Schedule.objects.filter(expire=False)
    for schedule in nonExpire:
        if schedule.date<datetime.now():
            nonExpire[0].expire=True
            nonExpire[0].save()