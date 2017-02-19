# coding=UTF8
from django.shortcuts import render, get_object_or_404
from models import Member, Savelog, Food, Drink, Schedule, Catalog, FoodOrder, DrinkOrder
from models import Category

from .forms import MemberForm, PicForm, CatalogForm, FoodForm
from django.shortcuts import render_to_response, RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required

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
                FoodOrder.objects.create(memberName=de_member,scheduleName=schedule,foodName=name,num=num,date=now,price=count)
        
        if request.POST.get('drink-name'):
            drink = request.POST['drink-name']
            remark = request.POST['sugar']+request.POST['ice']+request.POST['drink-comment']
            price = request.POST['drink-price']
            DrinkOrder.objects.create(memberName=de_member,scheduleName=schedule,drinking=drink,num=1,remark=remark,date=now,price=price)
        
        return render(request, 'bandongo/frontend_markDetail.html', {'de_member': de_member,'finish_order':finish_order})
       
    
    else:
        #order index
        #===get today's schedule part===
        
        schedules = Schedule.objects.filter(expire=False)
        schedule_name = None
        duedate = None
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
        # if duedate != None:
        #     duedate = duedate.strftime("%Y/%m/%d, %H:%M")
        return render(request, 'bandongo/frontend_markDetail.html', {'de_member': de_member,'list_food':list_food,'pic_beverage':pic_beverage,'schedule_name':schedule_name,'due_date':duedate})

def member_log(request,pk):
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
    
    return render(request, 'bandongo/frontend_memberLog.html',{'de_member':de_member,'save_total':save_total,'savelogs':savelogs,'cost_total':cost_total,'foods_logs':foods_logs,'drinks_logs':drinks_logs,'total_sum':total_sum})


def today_order(request,pk):
    de_member =  get_object_or_404(Member, pk=pk)
    today_foods = FoodOrder.objects.filter(memberName=pk, finish=False).order_by('date')
    today_drinks = DrinkOrder.objects.filter(memberName=pk, finish=False).order_by('date')
    # order_duedate = None
    # if not today_foods:
    #     print "empty orders"
    # else:
    #     order_duedate = Schedule.objects.filter(name=today_foods[0].scheduleName)[0].date
    #     order_duedate = order_duedate.strftime('%Y/%m/%d:')
    return render(request, 'bandongo/frontend_todayOrder.html',{'de_member':de_member,'today_foods':today_foods,'today_drinks':today_drinks })

def delete_food(request):
    now = datetime.now()
    order = FoodOrder.objects.get(id=request.POST['id'])
    order_duedate = Schedule.objects.filter(name=order.scheduleName)[0].date
    failmessage = "截止日期已過"
    success = "刪除成功"
    if now > order_duedate:
        FoodOrder.objects.get(id=request.POST['id']).delete()
        return HttpResponse(failmessage)
    else:
        return HttpResponse(success)





def delete_drink(request):
    now = datetime.now()
    order = FoodOrder.objects.get(id=request.POST['id'])
    order_duedate = Schedule.objects.filter(name=order.scheduleName)[0].date
    failmessage = "截止日期已過"
    success = "刪除成功"
    
    if now > order_duedate:
        DrinkOrder.objects.get(id=request.POST['id']).delete()
        return HttpResponse(failmessage)
    else:
        return HttpResponse(success)
    

def mark_select(request):
    path="/home/ubuntu/workspace/static/pic/homePic"
    today = datetime.now()
    s_latest = Schedule.objects.filter(date__date = today).order_by('-id')
        
    
    if os.path.exists(path) and len(os.listdir(path))>0:
        picPath="/static/pic/homePic/"+os.listdir(path)[0]
    else:
        picPath=None
    
    if request.method == "POST":
        if request.POST.get('member_name') != None:
            
            member_pk = request.POST.get('member_name')
            return redirect('bandongo.views.mark_detail', pk=member_pk)
        else:
            mark_list = list(Category.objects.all().values())
            for i in range(len(mark_list)):
                mark_list[i]['index']=i
           
            # mark_list = Member.objects.values_list('member_mark',flat=True).distinct()
            return render(request, 'bandongo/frontend_markSelect.html',{'mark_list':mark_list,'homePicPath': picPath,'s_latest':s_latest})
    mark_list = list(Category.objects.all().values())
    for i in range(len(mark_list)):
        mark_list[i]['index']=i
    

    
    # mark_list = Member.objects.values_list('member_mark',flat=True).distinct()
    return render(request, 'bandongo/frontend_markSelect.html',{'mark_list':mark_list, 'homePicPath': picPath, 's_latest':s_latest})

def today_statistic(request, pk):
    de_member =  get_object_or_404(Member, pk=pk)
    today = datetime.date(datetime.now())
    schedules = Schedule.objects.filter(date__date = today) #get latest record
    empty = False;
    if not schedules:
        foods = None;
        drinks = None;
        empty = True;
    else:
        foods = FoodOrder.objects.filter(scheduleName=schedules[0])
        drinks = DrinkOrder.objects.filter(scheduleName=schedules[0])
    return render(request, 'bandongo/frontend_todayStatistic.html',{'schedules':schedules,'de_member':de_member, 'foods':foods, 'drinks':drinks, 'empty':empty})


## backend_part
## page part
def homePage(request):
    return render(request, 'bandongo/backend_home.html',{})

def login(request):
    if request.user.is_authenticated(): 
        return HttpResponseRedirect('/backend')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_staff:
        auth.login(request, user)
        if request.GET.get('next'):
            return HttpResponseRedirect(request.GET['next'])
        else:
            return HttpResponseRedirect('/backend')
    else:
        return render(request, 'bandongo/backend_login.html',{})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/backend/')

@login_required(login_url='/backend/login/')
def setSchedulePage(request):
    drinks=Drink.objects.all()
    shops=Food.objects.all()
    catalogs=Catalog.objects.filter(foodShop=shops[0])
    return render(request, 'bandongo/backend_setSchedule.html',{'drinks':drinks, 'shops': shops, 'catalogs': catalogs})

@login_required(login_url='/backend/login/')
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

@login_required(login_url='/backend/login/')
def scheduleListPage(request):
    schedules=Schedule.objects.all()
    for i in range(len(schedules)):
        catalogs=Catalog.objects.filter(foodShop=schedules[i].food, choosed=True)
        schedules[i].catalogs=""
        for catalog in catalogs:
            schedules[i].catalogs+=catalog.name+", "
        
    return render(request, 'bandongo/backend_scheduleList.html',{'schedules': schedules, 'catalogs': catalogs})

@login_required(login_url='/backend/login/')
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
            drinkTotalPrice+=sum(map(lambda order: order.price, tempOrders))
        return render(request, 'bandongo/backend_order.html',{'schedule': schedule, 'foodBags': foodBags, 'foodOrders': foodOrders, 'foodTotalPrice': foodTotalPrice, 'drinkBags': drinkBags, 'drinkTotalPrice': drinkTotalPrice})
    except ObjectDoesNotExist:
        return render(request, 'bandongo/backend_order.html',{'schedule': None})

@login_required(login_url='/backend/login/')
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

@login_required(login_url='/backend/login/')
def addMemberPage(request):
    categories=Category.objects.all()
    return render(request, 'bandongo/backend_addMember.html',{'categories': categories})

@login_required(login_url='/backend/login/')
def editMemberPage(request, id):
    categories=Category.objects.all()
    member=Member.objects.get(id=id)
    return render(request, 'bandongo/backend_editMember.html',{'categories': categories, 'member': member})

@login_required(login_url='/backend/login/')
def memberListPage(request):
    members=Member.objects.order_by('remark')
    return render(request, 'bandongo/backend_memberList.html',{'members': members})

@login_required(login_url='/backend/login/')
def addValuePage(request):
    admins=Member.objects.filter(auth='admin')
    categories=Category.objects.all()
    members=Member.objects.filter(remark=categories[0])
    return render(request, 'bandongo/backend_addValue.html',{'admins': admins, 'categories': categories, 'members': members})

@login_required(login_url='/backend/login/')
def homePicPage(request):
    form = PicForm()
    return render(request, 'bandongo/backend_homePic.html',{'form': form})

@login_required(login_url='/backend/login/')
def addCatalogPage(request):
    form = CatalogForm()
    return render(request, 'bandongo/backend_addForm.html',{'form': form, 'action': "addCatalog", 'title': 'Add Catalog'})

@login_required(login_url='/backend/login/')
def addCatalogBatchPage(request):
    foodShops=Food.objects.all()
    return render(request, 'bandongo/backend_addCatalogBatch.html',{'foodShops': foodShops})

@login_required(login_url='/backend/login/')
def catalogListPage(request):
    catalogs=Catalog.objects.all().order_by("foodShop")
    return render(request, 'bandongo/backend_catalogList.html',{'catalogs': catalogs})

@login_required(login_url='/backend/login/')
def editCatalogPage(request, id):
    catalog=Catalog.objects.get(id=id)
    form = CatalogForm(instance=catalog)
    return render(request, 'bandongo/backend_addForm.html',{'form': form, 'title': 'Edit Catalog', 'action': 'editCatalog/'+id})

@login_required(login_url='/backend/login/')
def addFoodShopPage(request):
    form = FoodForm()
    return render(request, 'bandongo/backend_addForm.html',{'form': form, 'action': "addFood", 'title': 'Add Food Shop'})

@login_required(login_url='/backend/login/')
def shopListPage(request):
    shops = Food.objects.all()
    return render(request, 'bandongo/backend_shopList.html',{'shops': shops})

@login_required(login_url='/backend/login/')
def editShopPage(request, id):
    shop=Food.objects.get(id=id)
    form = FoodForm(instance=shop)
    return render(request, 'bandongo/backend_addForm.html',{'form': form, 'title': 'Edit Shop', 'action': 'editShop/'+id})


## function part
@login_required(login_url='/backend/login/')
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

@login_required(login_url='/backend/login/')
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

@login_required(login_url='/backend/login/')
def finishSchedule(request):
    checkExpire()
    schedule=Schedule.objects.get(id=request.POST["id"])
    if not schedule.arrived:
        return HttpResponse("The schedule is not arrived.")
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
        FoodOrder.objects.filter(scheduleName=schedule).update(finish=True)
        DrinkOrder.objects.filter(scheduleName=schedule).update(finish=True)
        
        return HttpResponse("Finish Schedule Successfully")

@login_required(login_url='/backend/login/')
def arriveSchedule(request):
    checkExpire()
    schedule=Schedule.objects.get(id=request.POST["id"])
    if not schedule.expire:
        return HttpResponse("The schedule is not expired.")
    else:
        schedule.arrived=True
        schedule.save();
        
        return HttpResponse("Bandon arrived.")

@login_required(login_url='/backend/login/')
def addMember(request):
    category=Category.objects.get(id=request.POST["category"])
    Member.objects.create(name=request.POST["name"], phone=request.POST["phone"], email=request.POST["email"], remark=category)
    return HttpResponse("Add Member Successfully")

@login_required(login_url='/backend/login/')
def editMember(request):
    member=Member.objects.get(id=request.POST["id"])
    member.name=request.POST["name"]
    member.phone=request.POST["phone"]
    member.email=request.POST["email"]
    member.remark=Category.objects.get(id=request.POST["category"])
    member.save()
    return HttpResponse("Edit Member Successfully")

@login_required(login_url='/backend/login/')
def deleteMember(request):
    member=Member.objects.get(id=request.POST["id"])
    if not member.saving == 0:
        return HttpResponse("saving")
    else:
        member.delete()
        return HttpResponse("success")

@login_required(login_url='/backend/login/')
def addValue(request):
    member=Member.objects.get(id=request.POST["member"])
    value=request.POST["value"]
    admin=Member.objects.get(id=request.POST["admin"])
    comment=request.POST["comment"]
    
    Savelog.objects.create(memberName=member, money=value, adminName=admin, comment=comment)
    member.member_saving+=int(value)
    member.save()
    return HttpResponse("Add Value Successfully")

@login_required(login_url='/backend/login/')
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

@login_required(login_url='/backend/login/')
def addCatalog(request):
    form = CatalogForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/backend/addCatalogPage")
    else:
        return HttpResponse("<script>alert('not valid upload')</script>")

@login_required(login_url='/backend/login/')
def addCatalogBatch(request):
    shop=Food.objects.get(id=request.POST["shop"])
    text=request.POST["input"]
    for line in text.split('\n'):
        temp=line.strip().split()
        Catalog.objects.create(foodShop=shop, name=temp[0], price=temp[1])

    return HttpResponse("Added successfully.")

def editCatalog(request, id):
    catalog=Catalog.objects.get(id=id)
    form = CatalogForm(request.POST, request.FILES, instance=catalog)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/backend/catalogListPage")
    else:
        return HttpResponse("<script>alert('not valid form')</script>")

def deleteCatalog(request):
    catalog=Catalog.objects.get(id=request.POST["id"])
    catalog.delete()
    return HttpResponse("Deleted successfully.")

@login_required(login_url='/backend/login/')
def addFood(request):
    form = FoodForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/backend/addFoodShopPage")
    else:
        return HttpResponse("<script>alert('not valid upload')</script>")

def editShop(request, id):
    shop=Food.objects.get(id=id)
    form = FoodForm(request.POST, request.FILES, instance=shop)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/backend/shopListPage")
    else:
        return HttpResponse("<script>alert('not valid form')</script>")

def deleteFood(request):
    food=Food.objects.get(id=request.POST["id"])
    food.delete()
    return HttpResponse("Deleted successfully.")

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
