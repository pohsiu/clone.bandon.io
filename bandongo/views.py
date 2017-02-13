from django.shortcuts import render, get_object_or_404
from models import Member, Savelog, Food, Drink, Schedule, Catalog, FoodOrder, DrinkOrder
from models import Category

from .forms import MemberForm, PicForm, CatalogForm
from django.shortcuts import render_to_response, RequestContext

from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse

from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from django.db.models import Sum

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime
from datetime import date #detail index used
from django.utils.dateparse import parse_datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

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
    member = get_object_or_404(Member, id=pk)
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






#related test
def filter_json(request):
    
    mark_list=Category.objects.all()
    marks = list(mark_list.values())
    # for i in range(len(marks)):
    #     marks[i]['index']=i
    models = []
    for mark in mark_list:
        models.append(list(Member.objects.all().filter(remark=mark).values()))
        
    return JsonResponse({'member_list': models, 'mark_list': marks})
    
def mark_detail_backup(request, pk):
    de_member = get_object_or_404(Member, pk=pk)
    now = datetime.now()
    finish_order = 'Y'
    if request.method =="POST":
        schedule = Schedule.objects.get(name=request.POST['schedule'])
        if request.POST['order-type'] == u'food':   # test the form type
            food_len = int(request.POST['food-len'])
            finish_order='food'
            for i in range(1, food_len+1):
                if request.POST['food-num'+unicode(i)] != '0':
                    # foodremark = ''
                    # if request.POST['food-remark'+unicode(i)] != '':
                    #     foodremark = request.POST['food-remark'+unicode(i)]
                    price = int(request.POST['food-price'+unicode(i)])
                    num = int(request.POST['food-num'+unicode(i)])
                    count    = price * num
                    name = Catalog.objects.get(name=request.POST['food-name'+unicode(i)])
                    FoodOrder.objects.create(memberName=de_member,scheduleName=schedule,foodName=name,num=num,date=now,price=count)
                    
            # print type(food_len)
            return render(request, 'bandongo/mark_detail.html', {'de_member': de_member,'finish_order':finish_order})
        elif request.POST['order-type'] == u'beverage':
            finish_order='beverage'
            if request.POST.get('drink-name'):
                drink = request.POST['drink-name']
                remark = request.POST['sugar']+request.POST['ice']
                price = request.POST['drink-price']
                DrinkOrder.objects.create(memberName=de_member,scheduleName=schedule,drinking=drink,num=1,remark=remark,date=now,price=price)
            
            return render(request, 'bandongo/mark_detail.html', {'de_member': de_member,'finish_order':finish_order})
        else:    
            return render(request, 'bandongo/mark_detail.html', {'de_member': de_member})
        
            
    
    else:
        #order index
        #===get today's schedule part===
        
        schedules = Schedule.objects.filter(expire=False)
        schedule_name = None
        if schedules:
            duedate = schedules[0].date
            if now < duedate:
                id_food = schedules[0].food
                id_beverage = schedules[0].drink.name
                list_food = Catalog.objects.filter(foodShop = id_food, choosed=True)
                pic_beverage = Drink.objects.filter(name = id_beverage)
                schedule_name = schedules[0].name
            else:
                list_food=''
                pic_beverage=''
        else:
            list_food=''
            pic_beverage=''
        
        
        return render(request, 'bandongo/mark_detail.html', {'de_member': de_member,'list_food':list_food,'pic_beverage':pic_beverage,'schedule_name':schedule_name})
    

def mark_detail(request, pk):
    de_member = get_object_or_404(Member, pk=pk)
    now = datetime.now()
    finish_order = 'Y'
    if request.method =="POST":
        schedule = Schedule.objects.get(name=request.POST['schedule'])
        food_len = int(request.POST['food-len'])
        finish_order='passed'
        for i in range(1, food_len+1):
            if request.POST['food-num'+unicode(i)] != '0':
                catalog = Catalog.objects.get(name=request.POST['food-name'+unicode(i)])
                price = catalog.price
                num = int(request.POST['food-num'+unicode(i)])
                count    = price * num
                name = catalog
                # print price
                FoodOrder.objects.create(memberName=de_member,scheduleName=schedule,foodName=name,num=num,date=now,price=count)
        
        if request.POST.get('drink-name'):
            drink = request.POST['drink-name']
            remark = request.POST['sugar']+request.POST['ice']
            price = request.POST['drink-price']
            DrinkOrder.objects.create(memberName=de_member,scheduleName=schedule,drinking=drink,num=1,remark=remark,date=now,price=price)
        
        return render(request, 'bandongo/mark_detail.html', {'de_member': de_member,'finish_order':finish_order})
       
    
    else:
        #order index
        #===get today's schedule part===
        
        schedules = Schedule.objects.filter(expire=False)
        schedule_name = None
        if schedules:
            duedate = schedules[0].date
            if now < duedate:
                id_food = schedules[0].food
                id_beverage = schedules[0].drink.name
                list_food = Catalog.objects.filter(foodShop = id_food, choosed=True)
                pic_beverage = Drink.objects.filter(name = id_beverage)
                schedule_name = schedules[0].name
            else:
                list_food=''
                pic_beverage=''
        else:
            list_food=''
            pic_beverage=''
        
        
        return render(request, 'bandongo/mark_detail.html', {'de_member': de_member,'list_food':list_food,'pic_beverage':pic_beverage,'schedule_name':schedule_name})

def mark_log(request,pk):
    de_member = get_object_or_404(Member, pk=pk)
    
    save_total = Savelog.objects.filter(memberName=pk).aggregate(save_total=Sum('money'))['save_total']
    if save_total == None:
        save_total = 0
    savelogs = Savelog.objects.filter(memberName=pk).order_by('tranDate')
    foods_total = FoodOrder.objects.filter(memberName=pk,finish=True).aggregate(foods_total=Sum('price'))['foods_total']
    drinks_total = DrinkOrder.objects.filter(memberName=pk,finish=True).aggregate(drinks_total=Sum('price'))['drinks_total']
    if foods_total == None:
        foods_total = 0
    if drinks_total == None:
        drinks_total = 0
    foods_logs = FoodOrder.objects.filter(memberName=pk, finish=True).order_by('date')
    drinks_logs = DrinkOrder.objects.filter(memberName=pk, finish=True).order_by('date')
    cost_total = foods_total + drinks_total
    total_sum = save_total - cost_total
    
    return render(request, 'bandongo/mark_log.html',{'de_member':de_member,'save_total':save_total,'savelogs':savelogs,'cost_total':cost_total,'foods_logs':foods_logs,'drinks_logs':drinks_logs,'total_sum':total_sum})


def mark_todayOrder(request,pk):
    de_member =  get_object_or_404(Member, pk=pk)
    today_foods = FoodOrder.objects.filter(memberName=pk, finish=False).order_by('date')
    today_drinks = DrinkOrder.objects.filter(memberName=pk, finish=False).order_by('date')
    return render(request, 'bandongo/mark_todayOrder.html',{'de_member':de_member,'today_foods':today_foods,'today_drinks':today_drinks})

def delete_food(request):
    FoodOrder.objects.get(id=request.POST['id']).delete()
    return HttpResponse("Delete Success")

def delete_drink(request):
    DrinkOrder.objects.get(id=request.POST['id']).delete()
    return HttpResponse("Delete Success")

def mark2(request):
    if request.method == "POST":
        if request.POST.get('member_name') != None:
            
            member_pk = request.POST.get('member_name')
            return redirect('bandongo.views.mark_detail', pk=member_pk)
        else:
            mark_list = list(Category.objects.all().values())
            for i in range(len(mark_list)):
                mark_list[i]['index']=i
           
            # mark_list = Member.objects.values_list('member_mark',flat=True).distinct()
            return render(request, 'bandongo/mark_select.html',{'mark_list':mark_list})
    mark_list = list(Category.objects.all().values())
    for i in range(len(mark_list)):
        mark_list[i]['index']=i
    path="/home/ubuntu/workspace/static/pic/homePic"
    if len(os.listdir(path))>0:
        picPath="/static/pic/homePic/"+os.listdir(path)[0]
    else:
        picPath=None
    # mark_list = Member.objects.values_list('member_mark',flat=True).distinct()
    return render(request, 'bandongo/mark_select.html',{'mark_list':mark_list, 'homePicPath': picPath})




## backend_part
## page part
def setSchedulePage(request):
    drinks=Drink.objects.all()
    shops=Food.objects.all()
    catalogs=Catalog.objects.filter(foodShop=shops[0])
    return render(request, 'bandongo/backend_setSchedule.html',{'drinks':drinks, 'shops': shops, 'catalogs': catalogs})

def editSchedulePage(request):
    nonFinish=Schedule.objects.filter(finish=False)
    if len(nonFinish)==0:
        return render(request, 'bandongo/backend_editSchedule.html',{})
    elif len(nonFinish)==1:
        shops=Food.objects.all()
        drinks=Drink.objects.all()
        for index in range(len(shops)):
            if shops[index]==nonFinish[0].food:
                shops[index].selected="selected"
                catalogs=Catalog.objects.filter(foodShop=shops[index])
                for index2 in range(len(catalogs)):
                    if catalogs[index2].choosed:
                        catalogs[index2].selected="selected"
                    else:
                        catalogs[index2].selected=""
            else:
                shops[index].selected=""
        for index in range(len(drinks)):
            if drinks[index]==nonFinish[0].drink:
                drinks[index].selected="selected"
            else:
                drinks[index].selected=""
        nonFinish[0].date=nonFinish[0].date.strftime("%Y-%m-%dT%H:%M")
        return render(request, 'bandongo/backend_editSchedule.html',{'schedule': nonFinish[0], 'shops':shops, 'catalogs': catalogs, 'drinks':drinks})
    else:
        print "bugbugbugbug"

def scheduleListPage(request):
    schedules=Schedule.objects.all()
    for i in range(len(schedules)):
        catalogs=Catalog.objects.filter(foodShop=schedules[i].food, choosed=True)
        schedules[i].catalogs=""
        for catalog in catalogs:
            schedules[i].catalogs+=catalog.name+", "
        
    return render(request, 'bandongo/backend_scheduleList.html',{'schedules': schedules, 'catalogs': catalogs})

def orderPage(request):
    checkExpire()
    try:
        schedule=Schedule.objects.get(finish=False)
        catalogs=Catalog.objects.filter(foodShop=schedule.food)
        foodBags=[]
        foodOrders=[]
        for catalog in catalogs:
            tempOrders=FoodOrder.objects.filter(scheduleName=schedule, foodName=catalog)
            count=0
            price=0
            for tempOrder in tempOrders:
                count+=tempOrder.num
                price+=tempOrder.price
            if count > 0:
                foodOrders.append({"foodName": catalog.name, "count": count, 'price': price})
        
        foodTotalPrice=0
        for i in range(3):
            foodBags.append([])
            for catalog in catalogs:
                tempOrders=FoodOrder.objects.filter(scheduleName=schedule, foodName=catalog, memberName__remark__bag=(i+1))
                count=0
                price=0
                for tempOrder in tempOrders:
                    count+=tempOrder.num
                    price+=tempOrder.price
                if count > 0:
                    foodBags[i].append({"foodName": catalog.name, "count": count, 'price': price})
                    foodTotalPrice+=price

        drinkBags=[]
        drinkTotalPrice=0
        for i in range(3):
            tempOrders=DrinkOrder.objects.filter(scheduleName=schedule, memberName__remark__bag=(i+1)).order_by('drinking', 'remark')
            drinkBags.append(tempOrders)
            print tempOrders
            drinkTotalPrice+=sum(map(lambda order: order.price, tempOrders))
        return render(request, 'bandongo/backend_order.html',{'schedule': schedule, 'foodBags': foodBags, 'foodOrders': foodOrders, 'foodTotalPrice': foodTotalPrice, 'drinkBags': drinkBags, 'drinkTotalPrice': drinkTotalPrice})
    except ObjectDoesNotExist:
        return render(request, 'bandongo/backend_order.html',{'schedule': None})

def orderDetailPage(request, id):
    checkExpire()
    try:
        schedule=Schedule.objects.get(id=id)
        foodBags=[]
        drinkBags=[]
        foodTotalPrice=0
        drinkTotalPrice=0

        for i in range(3):
            orders=FoodOrder.objects.filter(scheduleName=schedule, memberName__remark__bag=(i+1))
            for order in orders:
                foodTotalPrice+=order.price
            foodBags.append(orders)
        
        for i in range(3):
            orders=DrinkOrder.objects.filter(scheduleName=schedule, memberName__remark__bag=(i+1))
            for order in orders:
                drinkTotalPrice+=order.price
            drinkBags.append(orders)
        
        return render(request, 'bandongo/backend_orderDetail.html',{'schedule': schedule, 'foodBags': foodBags, 'foodTotalPrice': foodTotalPrice, 'drinkBags': drinkBags, 'drinkTotalPrice': drinkTotalPrice})
    except ObjectDoesNotExist:
        return render(request, 'bandongo/backend_orderDetail.html',{'schedule': None})

def addMemberPage(request):
    categories=Category.objects.all()
    return render(request, 'bandongo/backend_addMember.html',{'categories': categories})

def editMemberPage(request, id):
    categories=Category.objects.all()
    member=Member.objects.get(id=id)
    return render(request, 'bandongo/backend_editMember.html',{'categories': categories, 'member': member})

def memberListPage(request):
    members=Member.objects.order_by('remark')
    return render(request, 'bandongo/backend_memberList.html',{'members': members})

def addValuePage(request):
    admins=Member.objects.filter(auth='admin')
    categories=Category.objects.all()
    members=Member.objects.filter(remark=categories[0])
    return render(request, 'bandongo/backend_addValue.html',{'admins': admins, 'categories': categories, 'members': members})

def homePicPage(request):
    form = PicForm()
    return render(request, 'bandongo/backend_homePic.html',{'form': form})

def addCatalogPage(request):
    form = CatalogForm()
    return render(request, 'bandongo/backend_addCatalog.html',{'form': form})


## function part
def setSchedule(request):
    checkExpire()
    nonFinish=len(Schedule.objects.filter(finish=False))
    dueDatetime=parse_datetime(request.POST["dueDatetime"])
    bandon=Food.objects.get(id=request.POST["bandon"])
    drink=Drink.objects.get(id=request.POST["drink"])
    catalogs=request.POST.getlist("cata[]")
    if nonFinish==0:
        Schedule.objects.create(name=request.POST["schedule_name"], food=bandon, drink=drink, date=dueDatetime)
        Catalog.objects.all().update(choosed=False)
        for catalog in catalogs:
            temp=Catalog.objects.get(id=catalog)
            temp.choosed=True
            temp.save()
        return HttpResponse("Registered Schedule Successfully")
    else:
        return HttpResponse("Another schedule is not finished.")

def editSchedule(request):
    schedule=Schedule.objects.get(id=request.POST["id"])
    schedule.date=parse_datetime(request.POST["dueDatetime"])
    schedule.food=Food.objects.get(id=request.POST["bandon"])
    schedule.drink=Drink.objects.get(id=request.POST["drink"])
    schedule.name=request.POST["name"]
    schedule.save();
    
    catalogs=request.POST.getlist("catalogs[]")
    for catalog in catalogs:
        temp=Catalog.objects.get(id=catalog)
        temp.choosed=True
        temp.save()

    return HttpResponse("Edit Schedule Successfully")

def finishSchedule(request):
    checkExpire()
    schedule=Schedule.objects.get(id=request.POST["id"])
    if not schedule.expire:
        return HttpResponse("The schedule is not expired.")
    else:
        schedule.finish=True
        schedule.save();
        fOrders=FoodOrder.objects.filter(scheduleName=schedule)
        dOrders=DrinkOrder.objects.filter(scheduleName=schedule)
        for order in fOrders:
            member=order.memberName
            member.saving-=order.price
            member.save()
            order.finish=True
            order.save()
        for order in dOrders:
            member=order.memberName
            member.saving-=order.price
            member.save()
            order.finish=True
            order.save()
        
        return HttpResponse("Finish Schedule Successfully")

def addMember(request):
    category=Category.objects.get(id=request.POST["category"])
    Member.objects.create(name=request.POST["name"], phone=request.POST["phone"], email=request.POST["email"], remark=category)
    return HttpResponse("Add Member Successfully")

def editMember(request):
    member=Member.objects.get(id=request.POST["id"])
    member.name=request.POST["name"]
    member.phone=request.POST["phone"]
    member.email=request.POST["email"]
    member.remark=Category.objects.get(id=request.POST["category"])
    member.save()
    return HttpResponse("Edit Member Successfully")

def deleteMember(request):
    member=Member.objects.get(id=request.POST["id"])
    if not member.saving == 0:
        return HttpResponse("saving")
    else:
        member.delete()
        return HttpResponse("success")

def addValue(request):
    member=Member.objects.get(id=request.POST["member"])
    value=request.POST["value"]
    admin=Member.objects.get(id=request.POST["admin"])
    comment=request.POST["comment"]
    
    Savelog.objects.create(memberName=member, money=value, adminName=admin, comment=comment)
    member.member_saving+=int(value)
    member.save()
    return HttpResponse("Add Value Successfully")

def checkExpire():
    nonExpire=Schedule.objects.filter(expire=False)
    for schedule in nonExpire:
        if schedule.date<datetime.now():
            nonExpire[0].expire=True
        else:
            nonExpire[0].expire=False
        nonExpire[0].save()

def getCateMem(request):
    categories=Category.objects.all()
    members=[]
    for category in categories:
        members.append(list(Member.objects.filter(remark=category).values()))
    return JsonResponse({'categories': list(categories.values()), 'members': members})
    
def getShopCat(request):
    shops=Food.objects.all()
    catalogs=[]
    for shop in shops:
        catalogs.append(list(Catalog.objects.filter(foodShop=shop).values()))
    return JsonResponse({'shops': list(shops.values()), 'catalogs': catalogs})
    
def setHomePic(request):
    form = PicForm(request.POST, request.FILES)
    if form.is_valid():
        path="/home/ubuntu/workspace/static/pic/homePic"
        if len(os.listdir(path))>0:
            picPath=path+"/"+os.listdir(path)[0]
            default_storage.delete(picPath)
        homePicPath="/home/ubuntu/workspace/static/pic/homePic/"+form.cleaned_data['homePic'].name
        default_storage.save(homePicPath, form.cleaned_data['homePic'])
        return HttpResponseRedirect("/")
    else:
        return HttpResponse("<script>alert('not valid upload')</script>")

def addCatalog(request):
    form = CatalogForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/backend/addCatalogPage")
    else:
        return HttpResponse("<script>alert('not valid upload')</script>")