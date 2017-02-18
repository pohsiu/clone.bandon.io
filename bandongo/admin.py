from django.contrib import admin
from .models import Member
from .models import Savelog
from .models import Catalog
from .models import FoodOrder
from .models import Food
from .models import Drink
from .models import DrinkOrder
from .models import Schedule
from .models import Category
from .models import Notification






class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email','remark','auth','saving')
    search_fields = ('name','email')
class SavelogAdmin(admin.ModelAdmin):
    list_display = ('id', 'memberName','money','adminName','tranDate', 'comment')
    list_filter = ('tranDate',)
    # search_fields = ('member_name')
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','foodShop','pic','price', 'choosed')
    
  
    
class FoodOrderAdmin(admin.ModelAdmin):
    list_display = ('id','memberName', 'scheduleName','foodName','price','remark', 'num','date','finish')
    list_filter = ('date',)
    date_hierarchy = 'date'
    ordering = ('-date',)
class DrinkOrderAdmin(admin.ModelAdmin):
    list_display = ('id','memberName', 'scheduleName','drinking','price','remark', 'num','date','finish')
    list_filter = ('date',)
    date_hierarchy = 'date'
    ordering = ('-date',)
    
class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','pic','telephone','address','remark')
class DrinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','pic','telephone','address','remark')
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'food','drink','date','expire', 'arrived', 'finish')
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bag')
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'classification', 'subject', 'content', 'date', 'read')

admin.site.register(Member, MemberAdmin)
admin.site.register(Savelog, SavelogAdmin)
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(FoodOrder, FoodOrderAdmin)
admin.site.register(DrinkOrder, DrinkOrderAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Drink, DrinkAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Notification, NotificationAdmin)



