# coding=UTF8
from django.shortcuts import render, get_object_or_404
from models import Member, Savelog, Food, Drink, Schedule, Catalog, FoodOrder, DrinkOrder, Message
from models import Category, WishFood, WishDrink, Notification

from .forms import MemberForm, PicForm, CatalogForm, FoodForm, DrinkForm, DepartmentForm
from django.shortcuts import render_to_response, RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse

from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from django.db.models import Sum, Count

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from datetime import datetime, timedelta
from datetime import date #detail index used
from django.utils.dateparse import parse_datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.db.models import Q
import os
import json
import numpy as np
import jieba
import sys
from gensim.models.doc2vec import Doc2Vec


from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError



# reload(sys)
# sys.setdefaultencoding('utf-8')
# jieba.initialize()
# jieba.set_dictionary('bandongo/dict.txt.big')
# model = Doc2Vec.load('bandongo/womentalk_contents.doc2vec.model2')


# with open('bandongo/selected_ptt_comments_seg', 'r') as myf:
#     sentbank = myf.readlines()
# for i in range(len(sentbank)):                                                                                                                      
#     sentbank[i] = sentbank[i].replace('\n', ' ').split()
# with open('bandongo/selected_ptt_comments', 'r') as myf:
#     ansbank = myf.readlines()
# for i in range(len(sentbank)):                                                                                                                      
#     ansbank[i] = ansbank[i].replace('\n', ' ')


    
    
greeting_msg = Message.objects.filter(usage="greeting message")
msg_morning = Message.objects.filter(usage="greeting msg morning")
msg_noon = Message.objects.filter(usage="greeting msg noon")
msg_night = Message.objects.filter(usage="greeting msg night")
msg_midnight = Message.objects.filter(usage="greeting msg midnight")


def sendLineRobot(request):
    msg = request.POST['inputMsg']
    sendMsg(msg)

def sendMsg(msg):
    line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
    users = Member.objects.all()
    for user in users:
        if user.lineid:
            line_bot_api.push_message(user.lineid, TextSendMessage(text=msg))
    return "ok"

# Create your views here.
# def userList(request):
#     users=User.objects.all()
#     return render(request, 'bandongo/user_list.html', {'users':users})


def index_v2(request):
    home_message = Message.objects.filter(usage="home message")
    schedules = Schedule.objects.filter(finish=False).order_by('-id') #get latest record
    s_latest = schedules
    mark_list = list(Category.objects.all().values())
    if request.method == "POST":
        if request.POST.get('member_name') != None:
            
            member_pk = request.POST.get('member_name')
            return redirect('frontend_detail', pk=member_pk)
    empty = False
    
    if not schedules:
        foods = None;
        drinks = None;
        empty = True;
    else:
        foods = {}
        drinks = {}
        for i in schedules:
            foods[i.name] = FoodOrder.objects.filter(scheduleName=i).order_by('memberName__remark')
            drinks[i.name] = DrinkOrder.objects.filter(scheduleName=i).order_by('memberName__remark')
    
    
    for i in range(len(mark_list)):
        mark_list[i]['index']=i
    return render(request, 'bandongo/frontend_index_v2.html',{'s_latest':s_latest,'mark_list':mark_list,'home_message':home_message,'empty':empty,'drinks':drinks,'foods':foods})


def bot_reply(real_input):
    #max = 0
    answer = ""
    score_lst = []
    for i in range(len(sentbank)):
        sent = filter(lambda x: x in model.wv.vocab, sentbank[i])
        if len(sent)==0:
            #continue
            score_lst.append(0.0)
        else:
            #score = model.n_similarity(sent,real_input)
            score_lst.append(model.n_similarity(sent,real_input))
        #if score >= max:
        #    max = score
        #    answer = ansbank[i]
    pair = zip(score_lst, ansbank)
    pair.sort()
    sent_sorted = [x for y, x in pair]
    idx = np.random.choice(10, p=[1/55.0,2/55.0,3/55.0,4/55.0,5/55.0,6/55.0,7/55.0,8/55.0,9/55.0,10/55.0])
    answer = sent_sorted[-10:][idx]
    return ''.join(answer)
    

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

def post_msg(request):
    user_msg = request.POST['inputMsg']
    seg = jieba.cut(user_msg, cut_all=False)
    seg2 = " ".join(seg)
    real_input = filter(lambda x: x in model.wv.vocab, str(seg2).split())
    if len(real_input) == 0:
        return HttpResponse("你在說什麼？")
    else:
        robot_msg = bot_reply(real_input)
        return HttpResponse(robot_msg)

def frontend_robot(request,pk):
    de_member = get_object_or_404(Member, pk=pk)
    
    return render(request,'bandongo/frontend_robot.html',{'de_member':de_member,'greeting_msg':greeting_msg,'msg_morning':msg_morning,'msg_noon':msg_noon,'msg_night':msg_night,'msg_midnight':msg_midnight})
    
def check_order(request):
    schedule_id = request.POST['schedule_id']
    member_id = request.POST['member_id']
    foodorders = FoodOrder.objects.filter(scheduleName__id=schedule_id,memberName__id=member_id)
    drinkorders = DrinkOrder.objects.filter(scheduleName__id=schedule_id,memberName__id=member_id)
    if foodorders.exists() and (drinkorders.exists()):
        return HttpResponse("both")
    if (not foodorders.exists()) and drinkorders.exists():
        return HttpResponse("drink")
    if foodorders.exists() and (not drinkorders.exists()):
        return HttpResponse("food")
    if (not foodorders.exists()) and (not drinkorders.exists()):
        return HttpResponse("nothing")

def add_order(request):
    checkExpire()
    foodJson=json.loads(request.POST["foodJson"])
    # print foodJson
    now = datetime.now()
    schedule = Schedule.objects.get(id=request.POST['schedule_id'])
    member = Member.objects.get(id=request.POST['member_id'])
    success = "訂餐成功"
    fail = "統計時間已過"
    if now < schedule.date:
        for i in foodJson:
            if i['food_num'] != '0':
                catalog=Catalog.objects.get(id=i['catalog_id'])
                price = catalog.price
                num = int(i['food_num'])
                count = price * num
                FoodOrder.objects.create(memberName=member, scheduleName=schedule, foodName=catalog, num=num, date=now, price=count)
        
        if request.POST.get('drinkname'):
            print "working"
            drink = request.POST['drinkname']
            remark = request.POST['sugar']+request.POST['ice']+request.POST['drinkcomment']
            price = request.POST['drinkprice']
            DrinkOrder.objects.create(memberName=member,scheduleName=schedule,drinking=drink,num=1,remark=remark,date=now,price=price)
        
       
        return HttpResponse(success)
    else:
        return HttpResponse(fail)

def mark_detail(request, pk):
    checkExpire()
    de_member = get_object_or_404(Member, pk=pk)
    now = datetime.now()
    schedules = Schedule.objects.filter(expire=False)
    list_food = None
    pic_beverage = None
    duedate = None
    top3 = None
    if schedules:
        duedate = schedules[0].date
        if now < duedate:
            id_beverage = schedules[0].drink.name
            list_food = schedules[0].catalogs.all()
            pic_beverage = Drink.objects.filter(name = id_beverage)
            
            top3 = FoodOrder.objects.filter(scheduleName = schedules).values('foodName__name').annotate(s_sum = Sum('num')).order_by('-s_sum')[:3]
        else:
            schedules = None
    return render(request, 'bandongo/frontend_markDetail.html', {'de_member': de_member,'list_food':list_food,'pic_beverage':pic_beverage,'schedules':schedules,'due_date':duedate,'top3':top3,'greeting_msg':greeting_msg,'msg_morning':msg_morning,'msg_noon':msg_noon,'msg_night':msg_night,'msg_midnight':msg_midnight})




def member_log(request,pk):
    de_member = get_object_or_404(Member, pk=pk)
    money_tag = 'B'
    save_total = Savelog.objects.filter(memberName=pk).aggregate(save_total=Sum('money'))['save_total']
    if save_total == None:
        save_total = 0
    savelogs = Savelog.objects.filter(memberName=pk).order_by('-tranDate')
    savelogs_latest5 = savelogs[:5]
    
    savelogs_listDic = []
    for each in savelogs:
        flag = False
        for index in range(len(savelogs_listDic)):
            if each.tranDate.strftime('%Y年-%m月') == savelogs_listDic[index]['month']:
                savelogs_listDic[index]['saving'].append(each)
                savelogs_listDic[index]['sum'] = savelogs_listDic[index]['sum'] + int(each.money)
                flag = True
        if not flag:
            savelogs_listDic.append({"month":each.tranDate.strftime('%Y年-%m月'),"saving":[each],"sum": int(each.money)})
        
    
    
    foods_total = FoodOrder.objects.filter(memberName=pk,finish=True).aggregate(foods_total=Sum('price'))['foods_total']
    drinks_total = DrinkOrder.objects.filter(memberName=pk,finish=True).aggregate(drinks_total=Sum('price'))['drinks_total']
    if foods_total == None:
        foods_total = 0
    if drinks_total == None:
        drinks_total = 0
    foods_logs = FoodOrder.objects.filter(memberName=pk, finish=True).order_by('date')
    drinks_logs = DrinkOrder.objects.filter(memberName=pk, finish=True).order_by('date')
    
    
    combine_logs = list(foods_logs) + list(drinks_logs)
    sorted_logs = sorted(combine_logs, key=lambda x: x.scheduleName.date, reverse=True)
    listdic = []    
    for order in sorted_logs:
        flag = False
        for dicIndex in range(len(listdic)):
            if order.scheduleName == listdic[dicIndex]["schedule"]:
                listdic[dicIndex]["order"].append(order)
                flag=True
        if flag ==False:
            listdic.append({"schedule":order.scheduleName,"order":[order]})

    latest5 = listdic[:5]
    listDicMonth = []
    for each in sorted_logs:
        flag = False
        for dicIndex in range(len(listDicMonth)):
            if each.scheduleName.date.strftime('%Y年-%m月') == listDicMonth[dicIndex]['month']:
                listDicMonth[dicIndex]["order"].append(each)
                listDicMonth[dicIndex]["sum"] = listDicMonth[dicIndex]["sum"] + int(each.price)
                flag = True
        if not flag:
            listDicMonth.append({"month":each.scheduleName.date.strftime('%Y年-%m月'),"order":[each],"sum":int(each.price)})
    
    #creat each month sum dictionary
    # import itertools
    # gr = itertools.groupby(sorted_logs, lambda d:d.date.strftime('%Y年-%m月'))
    # dt = [{"month":m,"sum":sum([x.price for x in q])} for m, q in gr] #create listDic[{m1:sum(price1)},{m2:sum(price2}]
    
    # #insert each sum into specific month's dictionary
    # for index in range(len(listDicMonth)):
    #     for each in dt:
    #         if listDicMonth[index].get('month') == each.get('month'):
    #             if "sum" in listDicMonth[index]:
    #                 listDicMonth[index].append(each.get('sum'))
    #             else:
    #                 listDicMonth[index]['sum']=each.get('sum')
    
    


        
    cost_total = foods_total + drinks_total
    total_sum = save_total - cost_total
    
    if total_sum < 0:
        money_tag = 'R'
    
    return render(request, 'bandongo/frontend_memberLog.html',{'savelogs_latest5':savelogs_latest5,'savelogs_listDic':savelogs_listDic,'listDicMonth':listDicMonth,'latest5':latest5,'de_member':de_member,'save_total':save_total,'savelogs':savelogs,'cost_total':cost_total,'sorted_logs':sorted_logs,'total_sum':total_sum,'greeting_msg':greeting_msg,'money_tag':money_tag,'msg_morning':msg_morning,'msg_noon':msg_noon,'msg_night':msg_night,'msg_midnight':msg_midnight})

def today_order(request,pk):
    de_member =  get_object_or_404(Member, pk=pk)
    today_foods = FoodOrder.objects.filter(memberName=pk, finish=False).order_by('date')
    today_drinks = DrinkOrder.objects.filter(memberName=pk, finish=False).order_by('date')
    
    return render(request, 'bandongo/frontend_todayOrder.html',{'de_member':de_member,'today_foods':today_foods,'today_drinks':today_drinks,'greeting_msg':greeting_msg,'msg_morning':msg_morning,'msg_noon':msg_noon,'msg_night':msg_night,'msg_midnight':msg_midnight})

def delete_food(request):
    checkExpire()
    now = datetime.now()
    order = FoodOrder.objects.get(id=request.POST['id'])
    order_duedate = Schedule.objects.filter(name=order.scheduleName)[0].date
    failmessage = "截止日期已過，訂單無法刪除"
    success = "訂單刪除成功"
    if now > order_duedate:
        
        return HttpResponse(failmessage)
    else:
        FoodOrder.objects.get(id=request.POST['id']).delete()
        return HttpResponse(success)





def delete_drink(request):
    checkExpire()
    now = datetime.now()
    order = DrinkOrder.objects.get(id=request.POST['id'])
    order_duedate = Schedule.objects.filter(name=order.scheduleName)[0].date
    failmessage = "截止日期已過，訂單無法刪除"
    success = "訂單刪除成功"
    
    if now > order_duedate:
        return HttpResponse(failmessage)
    else:
        DrinkOrder.objects.get(id=request.POST['id']).delete()
        return HttpResponse(success)
    

def mark_select(request):
    path="/home/ubuntu/workspace/static/pic/homePic"
    s_latest = Schedule.objects.all().order_by('-id')
    
    home_message = Message.objects.filter(usage="home message")
    
    if os.path.exists(path) and len(os.listdir(path))>0:
        picPath="/static/pic/homePic/"+os.listdir(path)[0]
    else:
        picPath=None
    
    if request.method == "POST":
        if request.POST.get('member_name') != None:
            
            member_pk = request.POST.get('member_name')
            return redirect('frontend_detail', pk=member_pk)
        else:
            mark_list = list(Category.objects.all().values())
            for i in range(len(mark_list)):
                mark_list[i]['index']=i
            
            return render(request, 'bandongo/frontend_markSelect.html',{'mark_list':mark_list,'homePicPath': picPath,'s_latest':s_latest,'home_message':home_message})
    mark_list = list(Category.objects.all().values())
    for i in range(len(mark_list)):
        mark_list[i]['index']=i

    return render(request, 'bandongo/frontend_markSelect.html',{'mark_list':mark_list, 'homePicPath': picPath, 's_latest':s_latest,'home_message':home_message})

def today_statistic(request, pk):
    de_member =  get_object_or_404(Member, pk=pk)
    schedules = Schedule.objects.filter(finish=False).order_by('-id') #get latest record
    empty = False
    s_len = len(schedules)
    if not schedules:
        foods = None;
        drinks = None;
        empty = True;
    else:
        foods = {}
        drinks = {}
        for i in schedules:
            foods[i.name] = FoodOrder.objects.filter(scheduleName=i).order_by('memberName__remark')
            drinks[i.name] = DrinkOrder.objects.filter(scheduleName=i).order_by('memberName__remark')
    return render(request, 'bandongo/frontend_todayStatistic.html',{'schedules':schedules,'de_member':de_member, 'foods':foods, 'drinks':drinks, 'empty':empty,'s_len':range(s_len),'greeting_msg':greeting_msg,'msg_morning':msg_morning,'msg_noon':msg_noon,'msg_night':msg_night,'msg_midnight':msg_midnight})

def wish_meal(request, pk):
    de_member = get_object_or_404(Member, pk=pk)
    foodshops = Food.objects.all()
    drinkshops = Drink.objects.all()


    return render(request, 'bandongo/frontend_wishMeal.html',{'de_member':de_member,'foodshops':foodshops,'drinkshops':drinkshops,'greeting_msg':greeting_msg,'msg_morning':msg_morning,'msg_noon':msg_noon,'msg_night':msg_night,'msg_midnight':msg_midnight})


def add_feedback(request):
    member = Member.objects.get(id=request.POST['id'])
    feedback = request.POST['feedback']
    now = datetime.now()
    Notification.objects.create(classification=2,subject=member,content=feedback,date=now)
    msg= "您的心聲我們聽到了，相信您的付出會使系統變的更完善~"
    return HttpResponse(msg)

def add_text_meal(request):
    member = Member.objects.get(id=request.POST['id'])
    now = datetime.now()
    if request.POST['food']:
        textFood = request.POST['food']
        Notification.objects.create(classification=2,subject=member,content=textFood,date=now)
    if request.POST['drink']:
        textDrink = request.POST['drink']
        Notification.objects.create(classification=2,subject=member,content=textDrink,date=now)
    responseMsg = "您的心聲我們聽到了，相信您的付出會使餐飲變的更美好~"
    
    return HttpResponse(responseMsg)

def add_wish_meal(request):
    
    today = date.today()
    member = Member.objects.get(id=request.POST['id'])
    failmessage = "一天只能許一次願喔~"
    success = "許願成功，心誠則靈..."
    
    testFood = WishFood.objects.filter(member=member, date=today)
    testDrink = WishDrink.objects.filter(member=member, date=today)
    
    
    
    if not testFood and (not testDrink):
        food = Food.objects.get(id=request.POST['food'])
        
        WishFood.objects.create(member=member,food=food,date=today)
        if request.POST['drink'] != '0':
            drink = Drink.objects.get(id=request.POST['drink'])
            WishDrink.objects.create(member=member,drink=drink,date=today)
        return HttpResponse(success)
        
    else:
        return HttpResponse(failmessage)
    
def terms_of_use(request, pk):
    de_member = get_object_or_404(Member, pk=pk)
    terms = Message.objects.filter(usage="Terms of Use")
    return render(request,'bandongo/frontend_termsOfUse.html',{'de_member':de_member,'greeting_msg':greeting_msg,'terms':terms,'msg_morning':msg_morning,'msg_noon':msg_noon,'msg_night':msg_night,'msg_midnight':msg_midnight})


## backend_part
## page part
def homePage(request):
    members=Member.objects.all()
    notifications=Notification.objects.filter(read=False).order_by('-date')
    return render(request, 'bandongo/backend_home.html',{'balance': sum(map(lambda member: member.saving, members)), 'notifications': notifications})

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
    checkExpire()
    drinks=Drink.objects.all()
    shops=Food.objects.all()
    catalogs=Catalog.objects.filter(foodShop=shops[0])
    return render(request, 'bandongo/backend_setSchedule.html',{'drinks':drinks, 'shops': shops, 'catalogs': catalogs})

@login_required(login_url='/backend/login/')
def editSchedulePage(request):
    checkExpire()
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
                    if catalogs[index2] in nonFinish[0].catalogs.all():
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
def scheduleListPage(request, page):
    checkExpire()
    schedules=Schedule.objects.all().order_by('-id')
    page=int(page)
    pages=[]
    for i in range(len(schedules)/10+1):
        pages.append(i+1)
    if page*10-10>len(schedules):
        print "page error"
    elif page*10>len(schedules) and len(schedules)>page*10-10:
        return render(request, 'bandongo/backend_scheduleList.html',{'schedules': schedules[page*10-10:], 'pages': pages, 'curPage': page})
    else:
        return render(request, 'bandongo/backend_scheduleList.html',{'schedules': schedules[page*10-10:page*10], 'pages': pages, 'curPage': page})
    
    

@login_required(login_url='/backend/login/')
def emergencyPage(request):
    schedule=Schedule.objects.filter(finish=False)
    if len(schedule)>0:
        schedule=schedule[0]
    shops=Food.objects.all()
    catalogs=Catalog.objects.filter(foodShop=shops[0])
    return render(request, 'bandongo/backend_emergency.html',{'shops': shops, 'catalogs': catalogs, 'schedule': schedule})


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
        foodTotalCount=0
        for i in range(3):
            foodBags.append({})
            foodBags[i]["orders"]=[]
            foodBags[i]["count"]=0
            for catalog in catalogs:
                tempOrders=FoodOrder.objects.filter(scheduleName=schedule, foodName=catalog, memberName__remark__bag=(i+1))
                count=0
                price=0
                for tempOrder in tempOrders:
                    count+=tempOrder.num
                    price+=tempOrder.price
                if count > 0:
                    foodBags[i]["orders"].append({"foodName": catalog.name, "count": count, 'price': price})
                    foodBags[i]["count"]+=count
                    foodTotalPrice+=price
                    foodTotalCount+=count

        drinkBags=[]
        drinkTotalPrice=0
        drinkTotalCount=0
        for i in range(3):
            drinkBags.append({})
            tempOrders=DrinkOrder.objects.filter(scheduleName=schedule, memberName__remark__bag=(i+1)).order_by('drinking', 'remark')
            drinkBags[i]["orders"]=tempOrders
            drinkBags[i]["count"]=sum(map(lambda order: order.num, tempOrders))
            drinkTotalPrice+=sum(map(lambda order: order.price, tempOrders))
            drinkTotalCount+=sum(map(lambda order: order.num, tempOrders))

        return render(request, 'bandongo/backend_order.html',{'schedule': schedule, 'foodBags': foodBags, 'foodOrders': foodOrders, 'foodTotalPrice': foodTotalPrice, 'foodTotalCount': foodTotalCount, 'drinkBags': drinkBags, 'drinkTotalPrice': drinkTotalPrice, 'drinkTotalCount': drinkTotalCount})
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
            orders=FoodOrder.objects.filter(scheduleName=schedule, memberName__remark__bag=(i+1)).order_by('memberName__remark')
            num=0
            for order in orders:
                foodTotalPrice+=order.price
                num+=order.num
            foodBags.append({'orders': orders, 'num': num})
        
        for i in range(3):
            orders=DrinkOrder.objects.filter(scheduleName=schedule, memberName__remark__bag=(i+1)).order_by('memberName__remark')
            num=0
            for order in orders:
                drinkTotalPrice+=order.price
                num+=order.num
            drinkBags.append({'orders': orders, 'num': num})
        
        categories=Category.objects.all()
        members=Member.objects.filter(remark=categories[0])
        
        return render(request, 'bandongo/backend_orderDetail.html',{'schedule': schedule, 'foodBags': foodBags, 'foodTotalPrice': foodTotalPrice, 'drinkBags': drinkBags, 'drinkTotalPrice': drinkTotalPrice, 'categories': categories, 'members': members})
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
    remarks=Category.objects.all()
    members=[]
    for remark in remarks:
        members.append(Member.objects.filter(remark=remark))
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
    foods=Food.objects.all()
    catalogs=[]
    for food in foods:
        catalogs.append(Catalog.objects.filter(foodShop=food))
    return render(request, 'bandongo/backend_catalogList.html',{'catalogs': catalogs})

@login_required(login_url='/backend/login/')
def catalogChangePricePage(request):
    try:
        schedule=Schedule.objects.get(finish=False)
        catalogs=Catalog.objects.filter(foodShop=schedule.food)
        
    except ObjectDoesNotExist:
        schedule=None
        catalogs=[]
        
    return render(request, 'bandongo/backend_catalogChangePrice.html',{'schedule': schedule, 'catalogs': catalogs})

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
def foodShopListPage(request):
    shops = Food.objects.all()
    return render(request, 'bandongo/backend_foodShopList.html',{'shops': shops})

@login_required(login_url='/backend/login/')
def editFoodShopPage(request, id):
    shop=Food.objects.get(id=id)
    form = FoodForm(instance=shop)
    return render(request, 'bandongo/backend_addForm.html',{'form': form, 'title': 'Edit Food Shop', 'action': 'editFoodShop/'+id})

@login_required(login_url='/backend/login/')
def addDrinkShopPage(request):
    form = DrinkForm()
    return render(request, 'bandongo/backend_addForm.html',{'form': form, 'action': "addDrink", 'title': 'Add Drink Shop'})

@login_required(login_url='/backend/login/')
def drinkShopListPage(request):
    shops = Drink.objects.all()
    return render(request, 'bandongo/backend_drinkShopList.html',{'shops': shops})

@login_required(login_url='/backend/login/')
def editDrinkShopPage(request, id):
    shop=Drink.objects.get(id=id)
    form = FoodForm(instance=shop)
    return render(request, 'bandongo/backend_addForm.html',{'form': form, 'title': 'Edit Drink Shop', 'action': 'editDrinkShop/'+id})

@login_required(login_url='/backend/login/')
def messagePage(request):
    messages=Message.objects.all()
    return render(request, 'bandongo/backend_message.html',{'messages': messages})
    
@login_required(login_url='/backend/login/')
def instantMsg(request):
    
    return render(request, 'bandongo/backend_instantMsg.html')

@login_required(login_url='/backend/login/')
def wishPage(request):
    foodCount = WishFood.objects.filter(realized=False).values('food__name').annotate(num=Count('food__name')).order_by('-num')
    drinkCount = WishDrink.objects.filter(realized=False).values('drink__name').annotate(num=Count('drink__name')).order_by('-num')
    
    return render(request, 'bandongo/backend_wish.html',{'foods': foodCount, 'drinks': drinkCount})

@login_required(login_url='/backend/login/')
def savelogPage(request):
    savelogs=Savelog.objects.order_by('-id')[:10]
    
    return render(request, 'bandongo/backend_savelog.html',{'logs': savelogs})

@login_required(login_url='/backend/login/')
def addDepartmentPage(request):
    form = DepartmentForm()
    return render(request, 'bandongo/backend_addForm.html',{'form': form, 'action': "addDepartment", 'title': 'Add Department'})

@login_required(login_url='/backend/login/')
def departmentListPage(request):
    departments=Category.objects.all().order_by('bag')
    return render(request, 'bandongo/backend_departmentList.html',{'departments': departments})

@login_required(login_url='/backend/login/')
def editDepartmentPage(request, id):
    department=Category.objects.get(id=id)
    form = DepartmentForm(instance=department)
    return render(request, 'bandongo/backend_addForm.html',{'form': form, 'title': 'Edit Department', 'action': 'editDepartment/'+id})

@login_required(login_url='/backend/login/')
def notificationPage(request, page):
    nots=Notification.objects.all().order_by("-id")
    page=int(page)
    pages=[]
    for i in range(len(nots)/10+1):
        pages.append(i+1)
    if page*10-10>len(nots):
        print "page error"
    elif page*10>len(nots) and len(nots)>page*10-10:
        return render(request, 'bandongo/backend_notification.html',{'nots': nots[page*10-10:], 'pages': pages, 'curPage': page})
    else:
        return render(request, 'bandongo/backend_notification.html',{'nots': nots[page*10-10:page*10], 'pages': pages, 'curPage': page})

@login_required(login_url='/backend/login/')
def chuChienPayPage(request):
    admins=Member.objects.filter(auth='admin')
    categories=Category.objects.all()
    members=Member.objects.filter(remark=categories[0])
    return render(request, 'bandongo/backend_pay.html',{'admins': admins, 'categories': categories, 'members': members})


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
        schedule=Schedule.objects.create(name=request.POST["schedule_name"], food=bandon, drink=drink, date=dueDatetime)
        schedule.catalogs.set(Catalog.objects.filter(id__in=catalogs))
        head = "<"+request.POST["schedule_name"].encode('utf-8')+">"
        msg = head+"\n"+"吃:"+bandon.name.encode('utf-8')+"\n喝:"+drink.name.encode('utf-8')
        sendMsg(msg)
        return HttpResponse("Registered Schedule Successfully")
    else:
        return HttpResponse("Another schedule is not finished.")

@login_required(login_url='/backend/login/')
def editSchedule(request):

    schedule=Schedule.objects.get(id=request.POST["id"])
    schedule.name=request.POST["name"]
    schedule.date=parse_datetime(request.POST["dueDatetime"])
    schedule.food=Food.objects.get(id=request.POST["bandon"])
    catalogs=request.POST.getlist("catalogs[]")
    schedule.catalogs.set(Catalog.objects.filter(id__in=catalogs))

    # delete not chosen catalog orders
    FoodOrder.objects.filter(scheduleName=schedule).exclude(foodName__in=schedule.catalogs.all()).delete()
    if not schedule.drink==Drink.objects.get(id=request.POST["drink"]):
        DrinkOrder.objects.filter(scheduleName=schedule).delete()
    schedule.drink=Drink.objects.get(id=request.POST["drink"])
    schedule.save()
    checkExpire()

    return HttpResponse("Edit Schedule Successfully")

@login_required(login_url='/backend/login/')
def finishSchedule(request):
    checkExpire()
    schedule=Schedule.objects.get(id=request.POST["id"])
    if not (schedule.foodArrived and schedule.drinkArrived and schedule.expire):
        return HttpResponse("The schedule is not arrived or expired.")
    elif not schedule.finish:
        schedule.finish=True
        schedule.save();
        fOrders=FoodOrder.objects.filter(scheduleName=schedule, finish=False)
        dOrders=DrinkOrder.objects.filter(scheduleName=schedule, finish=False)
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

        WishFood.objects.filter(realized=False, food=schedule.food).update(realized=True)
        WishDrink.objects.filter(realized=False, drink=schedule.drink).update(realized=True)
        
        return HttpResponse("Finish Schedule Successfully")

def foodArrive(request):
    checkExpire()
    schedule=Schedule.objects.get(id=request.POST["id"])
    if not schedule.expire:
        return HttpResponse("The schedule is not expired.")
    else:
        schedule.foodArrived=True
        schedule.save();
        
        sendMsg("便當到囉~")
        return HttpResponse("Bandon arrived.")
    
def drinkArrive(request):
    checkExpire()
    schedule=Schedule.objects.get(id=request.POST["id"])
    if not schedule.expire:
        return HttpResponse("The schedule is not expired.")
    else:
        schedule.drinkArrived=True
        schedule.save();
        
        sendMsg("飲料到囉~")
        return HttpResponse("Drink arrived.")

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
    member.saving+=int(value)
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
        return HttpResponseRedirect("/backend/addCatalogPage/")
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

@login_required(login_url='/backend/login/')
def editCatalog(request, id):
    catalog=Catalog.objects.get(id=id)
    form = CatalogForm(request.POST, request.FILES, instance=catalog)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/backend/catalogListPage/")
    else:
        return HttpResponse("<script>alert('not valid form')</script>")

@login_required(login_url='/backend/login/')
def catalogChangePrice(request):
    catalogs=Catalog.objects.filter(id__in=request.POST.getlist("catalog[]"))
    price=int(request.POST["price"])
    for catalog in catalogs:
        catalog.price+=price
        catalog.save()
        for order in FoodOrder.objects.filter(scheduleName__finish=False, foodName=catalog):
            order.price=order.foodName.price*order.num
            order.save()
    return HttpResponse("Change price successfully.")

@login_required(login_url='/backend/login/')
def deleteCatalog(request):
    catalog=Catalog.objects.get(id=request.POST["id"])
    catalog.delete()
    return HttpResponse("Deleted successfully.")

@login_required(login_url='/backend/login/')
def addFood(request):
    form = FoodForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/backend/addFoodShopPage/")
    else:
        return HttpResponse("<script>alert('not valid upload')</script>")

@login_required(login_url='/backend/login/')
def editFoodShop(request, id):
    shop=Food.objects.get(id=id)
    form = FoodForm(request.POST, request.FILES, instance=shop)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/backend/foodShopListPage/")
    else:
        return HttpResponse("<script>alert('not valid form')</script>")

@login_required(login_url='/backend/login/')
def deleteFoodShop(request):
    food=Food.objects.get(id=request.POST["id"])
    food.delete()
    return HttpResponse("Deleted successfully.")

@login_required(login_url='/backend/login/')
def addDrink(request):
    form = DrinkForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/backend/addDrinkShopPage/")
    else:
        return HttpResponse("<script>alert('not valid upload')</script>")

@login_required(login_url='/backend/login/')
def editDrinkShop(request, id):
    shop=Drink.objects.get(id=id)
    form = DrinkForm(request.POST, request.FILES, instance=shop)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/backend/drinkShopListPage/")
    else:
        return HttpResponse("<script>alert('not valid form')</script>")

@login_required(login_url='/backend/login/')
def deleteDrinkShop(request):
    drink=Drink.objects.get(id=request.POST["id"])
    drink.delete()
    return HttpResponse("Deleted successfully.")

@login_required(login_url='/backend/login/')
def emergency(request):
    schedule=Schedule.objects.filter(finish=False)
    if len(schedule)>0:
        schedule=schedule[0]
        catalog=Catalog.objects.get(id=request.POST["catalog"])
        schedule.food=catalog.foodShop
        schedule.save()
        for order in FoodOrder.objects.filter(scheduleName=schedule):
            order.foodName=catalog
            order.price=catalog.price*order.num
            order.save()

        return HttpResponse("Set emergency successfully.")
    else:
        return HttpResponse("No non-finished schedule")

@login_required(login_url='/backend/login/')
def setMessage(request):
    m=Message.objects.get(id=request.POST["message"])
    m.content=request.POST["content"]
    m.save()
    print m
    print m.content
    print request.POST["content"]
    return HttpResponse("Set message successfully.")

@login_required(login_url='/backend/login/')
def addDepartment(request):
    form = DepartmentForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse("<script>alert('add successfully'); window.location.replace('/backend/addDepartmentPage/')</script>")
    else:
        return HttpResponse("<script>alert('not valid form'); window.location.replace('/backend/departmentListPage/')</script>")

@login_required(login_url='/backend/login/')
def editDepartment(request, id):
    department=Category.objects.get(id=id)
    form = DepartmentForm(request.POST, instance=department)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/backend/departmentListPage/")
    else:
        return HttpResponse("<script>alert('not valid form')</script>")

@login_required(login_url='/backend/login/')
def deleteDepartment(request):
    department=Category.objects.get(id=request.POST["id"])
    department.delete()
    return HttpResponse("Deleted successfully.")

@login_required(login_url='/backend/login/')
def readNot(request):
    notification=Notification.objects.filter(id=request.POST["not"])
    if len(notification)==1:
        notification.update(read=True)
        return HttpResponse("Read successfully.")
    else:
        return HttpResponse("Database Error")
        
@login_required(login_url='/backend/login/')
def deleteFoodOrder(request):
    order=FoodOrder.objects.filter(id=request.POST["orderId"])
    if len(order)==1:
        bag=order[0].memberName.remark.bag
        count=order[0].num
        price=order[0].price
        order.delete()
        return JsonResponse({'count': count, 'price': price, 'bag': bag})
    else:
        return JsonResponse(None, safe=False)
        
@login_required(login_url='/backend/login/')
def deleteDrinkOrder(request):
    order=DrinkOrder.objects.filter(id=request.POST["orderId"])
    if len(order)==1:
        bag=order[0].memberName.remark.bag
        count=order[0].num
        price=order[0].price
        order.delete()
        return JsonResponse({'count': count, 'price': price, 'bag': bag})
    else:
        return JsonResponse(None, safe=False)

@login_required(login_url='/backend/login/')
def addFoodOrder(request):
    member=Member.objects.filter(id=request.POST["member"])
    catalog=Catalog.objects.filter(id=request.POST["catalog"])
    count=int(request.POST["count"])
    schedule=Schedule.objects.filter(finish=False)
    if len(member)==1 and len(catalog)==1 and len(schedule)==1:
        foodOrder=FoodOrder.objects.create(memberName=member[0], scheduleName=schedule[0], foodName=catalog[0], num=count, price=catalog[0].price*count)
        response={'id': foodOrder.id, 'remark': member[0].remark.name, 'member': member[0].name, 'catalog': catalog[0].name, 'count': count, 'price': catalog[0].price*count, 'bag': member[0].remark.bag}
        return JsonResponse(response)
    else:
        return JsonResponse(None, safe=False)

@login_required(login_url='/backend/login/')
def addDrinkOrder(request):
    member=Member.objects.filter(id=request.POST["member"])
    drinking=request.POST["drinking"]
    remark=request.POST["remark"]
    price=int(request.POST["price"])
    schedule=Schedule.objects.filter(finish=False)
    if len(member)==1 and len(schedule)==1:
        drinkOrder=DrinkOrder.objects.create(memberName=member[0], scheduleName=schedule[0], drinking=drinking, num=1, remark=remark, price=price)
        response={'id': drinkOrder.id, 'category': member[0].remark.name, 'member': member[0].name, 'drink': drinking, 'remark': remark, 'count': 1, 'price': price, 'bag': member[0].remark.bag}
        return JsonResponse(response)
    else:
        return JsonResponse(None, safe=False)

@login_required(login_url='/backend/login/')
def chuChienPay(request):
    memberR=Member.objects.get(id=request.POST["memberReceive"])
    memberP=Member.objects.get(id=request.POST["memberPay"])
    value=int(request.POST["value"])
    admin=Member.objects.get(id=request.POST["admin"])
    comment=request.POST["comment"]
    
    Savelog.objects.create(memberName=memberR, money=value, adminName=admin, comment=comment+" from "+memberP.name)
    Savelog.objects.create(memberName=memberP, money=-value, adminName=admin, comment=comment+" to "+memberR.name)
    memberR.saving+=value
    memberP.saving-=value
    memberR.save()
    memberP.save()
    return HttpResponse("Chu Chien Pay Successfully")
        
        
def checkExpire():
    nonFinish=Schedule.objects.filter(finish=False)
    for schedule in nonFinish:
        if schedule.date<datetime.now():
            schedule.expire=True
        else:
            schedule.expire=False
        schedule.save()

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

def getMessage(request):
    messages=list(Message.objects.all().values())
    return JsonResponse({'messages': messages})

def getScheduleCatalogs(request):
    schedule=Schedule.objects.filter(finish=False)
    if len(schedule)==1:
        catalogs=list(schedule[0].catalogs.values())
    else:
        catalogs=[]
    return JsonResponse({'catalogs': catalogs})
