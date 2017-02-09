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
    url(r'^log/(?P<pk>[0-9]+)/$',views.mark_log),
    url(r'^todayOrder/(?P<pk>[0-9]+)/$',views.mark_todayOrder),
    url(r'^$', views.mark2),
    
    url(r'^frontend/delete_food$', views.delete_food),
    
    #form selection json temp html 
    url(r'^mark/json_models' , views.filter_json),
    
    
    
    ## backend part
    ## url part
    url(r'^backend/$', views.setSchedulePage),
    url(r'^backend/setSchedulePage$', views.setSchedulePage),
    url(r'^backend/editSchedulePage$', views.editSchedulePage),
    url(r'^backend/scheduleListPage$', views.scheduleListPage),
    url(r'^backend/order$', views.orderPage),
    url(r'^backend/schedule/([0-9]+)$', views.orderDetailPage),
    url(r'^backend/addMemberPage$', views.addMemberPage),
    url(r'^backend/memberListPage$', views.memberListPage),
    url(r'^backend/addValuePage$', views.addValuePage),
    url(r'^backend/member/([0-9]+)$', views.editMemberPage),

    ## function part
    url(r'^backend/setSchedule$', views.setSchedule),
    url(r'^backend/editSchedule$', views.editSchedule),
    url(r'^backend/finishSchedule$', views.finishSchedule),
    url(r'^backend/addMember$', views.addMember),
    url(r'^backend/editMember$', views.editMember),
    url(r'^backend/addValue$', views.addValue),
    
    url(r'^getCateMem$', views.getCateMem),
    url(r'^getShopCat$', views.getShopCat),

    url(r'^admin/', admin.site.urls),
]
