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
    
    
    
   
    
    
    
    url(r'^robot/(?P<pk>[0-9]+)/$', views.frontend_robot, name='frontend_robot'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.mark_detail, name='frontend_detail'),
    url(r'^log/(?P<pk>[0-9]+)/$',views.member_log, name='frontend_log'),
    url(r'^todayOrder/(?P<pk>[0-9]+)/$',views.today_order, name='frontend_todayOrder'),
    url(r'^wish/(?P<pk>[0-9]+)/$',views.wish_meal, name='frontend_wish'),
    url(r'^terms/(?P<pk>[0-9]+)/$',views.terms_of_use, name='frontend_terms'),
    url(r'^todayStatistic/(?P<pk>[0-9]+)/$',views.today_statistic, name='frontend_todayStatistic'),
    
    # url(r'^test/$', views.index_v2),
    url(r'^$', views.index_v2),
    
    url(r'^frontend/delete_food$', views.delete_food),
    url(r'^frontend/delete_drink$', views.delete_drink),
    url(r'^frontend/add_wish_meal$', views.add_wish_meal),
    url(r'^frontend/add_text_meal$', views.add_text_meal),
    url(r'^frontend/add_feedback$', views.add_feedback),
    url(r'^frontend/add_order$', views.add_order),
    url(r'^frontend/check_order$', views.check_order),
    url(r'^frontend/post_msg$', views.post_msg),
    
    #form selection json temp html 
    url(r'^mark/json_models' , views.filter_json),
    
    
    
    ## backend part
    ## url part
    url(r'^backend/$', views.homePage),
    url(r'^backend/login/$', views.login),
    url(r'^backend/logout/$', views.logout),
    url(r'^backend/setSchedulePage/$', views.setSchedulePage),
    url(r'^backend/editSchedulePage/$', views.editSchedulePage),
    url(r'^backend/scheduleListPage/([0-9]+)/$', views.scheduleListPage),
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
    url(r'^backend/savelogPage/$', views.savelogPage),
    url(r'^backend/addDepartmentPage/$', views.addDepartmentPage),
    url(r'^backend/departmentListPage/$', views.departmentListPage),
    url(r'^backend/department/([0-9]+)/$', views.editDepartmentPage),
    url(r'^backend/notificationPage/([0-9]+)/$', views.notificationPage),
    url(r'^backend/chuChienPayPage/$', views.chuChienPayPage),
    
    ## function part
    url(r'^backend/setSchedule$', views.setSchedule),
    url(r'^backend/editSchedule$', views.editSchedule),
    url(r'^backend/finishSchedule$', views.finishSchedule),
    url(r'^backend/foodArrive$', views.foodArrive),
    url(r'^backend/drinkArrive$', views.drinkArrive),
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
    url(r'^backend/addDepartment$', views.addDepartment),
    url(r'^backend/editDepartment/([0-9]+)$', views.editDepartment),
    url(r'^backend/deleteDepartment$', views.deleteDepartment),
    url(r'^backend/readNot$', views.readNot),
    url(r'^backend/deleteFoodOrder$', views.deleteFoodOrder),
    url(r'^backend/deleteDrinkOrder$', views.deleteDrinkOrder),
    url(r'^backend/addFoodOrder$', views.addFoodOrder),
    url(r'^backend/addDrinkOrder$', views.addDrinkOrder),
    url(r'^backend/chuChienPay$', views.chuChienPay),
    
    url(r'^getCateMem$', views.getCateMem),
    url(r'^getShopCat$', views.getShopCat),
    url(r'^getMessage$', views.getMessage),
    url(r'^getScheduleCatalogs$', views.getScheduleCatalogs),

    url(r'^admin/', admin.site.urls),
]
