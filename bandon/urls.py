"""bandon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from bandongo import views

# from pratest import views2



urlpatterns = [
    # url(r'^$', views.userList, name='home'),
    # url(r'^user_list/', views.userList, name='home'),
    
    
    
    url(r'^list/', views.memberList),
    url(r'^member/(?P<pk>[0-9]+)/$', views.member_detail),
    url(r'^member/new/$', views.member_new, name='member_new'),
    url(r'^member/(?P<pk>[0-9]+)/edit/$', views.member_edit, name='member_edit'),
    
    
    
    
    url(r'^detail/(?P<pk>[0-9]+)/$', views.mark_detail),
    url(r'^log/(?P<pk>[0-9]+)/$',views.member_log),
    url(r'^todayOrder/(?P<pk>[0-9]+)/$',views.today_order),
    url(r'^wish/(?P<pk>[0-9]+)/$',views.wish_meal),
    url(r'^terms/(?P<pk>[0-9]+)/$',views.terms_of_use),
    url(r'^todayStatistic/(?P<pk>[0-9]+)/$',views.today_statistic),
    url(r'^$', views.mark_select),
    
    url(r'^frontend/delete_food$', views.delete_food),
    url(r'^frontend/delete_drink$', views.delete_drink),
    url(r'^frontend/add_wish_meal$', views.add_wish_meal),
    url(r'^frontend/add_order$', views.add_order),
    url(r'^frontend/check_order$', views.check_order),
    
    #form selection json temp html 
    url(r'^mark/json_models' , views.filter_json),
    
    
    
    ## backend part
    ## url part
    url(r'^backend/$', views.homePage),
    url(r'^backend/login/$', views.login),
    url(r'^backend/logout/$', views.logout),
    url(r'^backend/setSchedulePage/$', views.setSchedulePage),
    url(r'^backend/editSchedulePage/$', views.editSchedulePage),
    url(r'^backend/scheduleListPage/$', views.scheduleListPage),
    url(r'^backend/emergencyPage/$', views.emergencyPage),
    url(r'^backend/order/$', views.orderPage),
    url(r'^backend/schedule/([0-9]+)/$', views.orderDetailPage),
    url(r'^backend/addMemberPage/$', views.addMemberPage),
    url(r'^backend/memberListPage/$', views.memberListPage),
    url(r'^backend/addValuePage/$', views.addValuePage),
    url(r'^backend/member/([0-9]+)/$', views.editMemberPage),
    url(r'^backend/homePicPage/$', views.homePicPage),
    url(r'^backend/addCatalogPage/$', views.addCatalogPage),
    url(r'^backend/addCatalogBatchPage/$', views.addCatalogBatchPage),
    url(r'^backend/catalogListPage/$', views.catalogListPage),
    url(r'^backend/catalogChangePricePage/$', views.catalogChangePricePage),
    url(r'^backend/catalog/([0-9]+)/$', views.editCatalogPage),
    url(r'^backend/addFoodShopPage/$', views.addFoodShopPage),
    url(r'^backend/foodShopListPage/$', views.foodShopListPage),
    url(r'^backend/addDrinkShopPage/$', views.addDrinkShopPage),
    url(r'^backend/drinkShopListPage/$', views.drinkShopListPage),
    url(r'^backend/foodShop/([0-9]+)/$', views.editFoodShopPage),
    url(r'^backend/drinkShop/([0-9]+)/$', views.editDrinkShopPage),
    url(r'^backend/messagePage/$', views.messagePage),
    url(r'^backend/wishPage/$', views.wishPage),
    
    ## function part
    url(r'^backend/setSchedule$', views.setSchedule),
    url(r'^backend/editSchedule$', views.editSchedule),
    url(r'^backend/finishSchedule$', views.finishSchedule),
    url(r'^backend/arriveSchedule$', views.arriveSchedule),
    url(r'^backend/addMember$', views.addMember),
    url(r'^backend/editMember$', views.editMember),
    url(r'^backend/deleteMember$', views.deleteMember),
    url(r'^backend/addValue$', views.addValue),
    url(r'^backend/setHomePic$', views.setHomePic),
    url(r'^backend/addCatalog$', views.addCatalog),
    url(r'^backend/addCatalogBatch$', views.addCatalogBatch),
    url(r'^backend/editCatalog/([0-9]+)$', views.editCatalog),
    url(r'^backend/catalogChangePrice$', views.catalogChangePrice),
    url(r'^backend/deleteCatalog$', views.deleteCatalog),
    url(r'^backend/addFood$', views.addFood),
    url(r'^backend/editFoodShop/([0-9]+)$', views.editFoodShop),
    url(r'^backend/deleteFoodShop$', views.deleteFoodShop),
    url(r'^backend/addDrink$', views.addDrink),
    url(r'^backend/editDrinkShop/([0-9]+)$', views.editDrinkShop),
    url(r'^backend/deleteDrinkShop$', views.deleteDrinkShop),
    url(r'^backend/emergency$', views.emergency),
    url(r'^backend/setMessage$', views.setMessage),
    
    url(r'^getCateMem$', views.getCateMem),
    url(r'^getShopCat$', views.getShopCat),
    url(r'^getMessage$', views.getMessage),
    url(r'^getScheduleCatalogs$', views.getScheduleCatalogs),

    url(r'^admin/', admin.site.urls),
]
