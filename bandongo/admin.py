from django.contrib import admin
from .models import Member
from .models import Savelog
from .models import Catalog
from .models import Orderlog
from .models import Shop
from .models import Beverage
from .models import Schedule
from .models import Category



from .models import VehicleBrand, VehicleModel


class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'member_phone', 'member_email','member_mark','member_auth','member_saving')
    search_fields = ('member_name','member_email')
class SavelogAdmin(admin.ModelAdmin):
    list_display = ('member_name','money','admin_name','tran_date', 'comment')
    list_filter = ('tran_date',)
    # search_fields = ('member_name')
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('name','shop_name','pic','price')
    
  
    
class OrderlogAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'schedule_name','catalog_name','orderprice', 'ordernum','orderdate')
    list_filter = ('orderdate',)
    date_hierarchy = 'orderdate'
    ordering = ('-orderdate',)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name','pic','telephone','address','remark')
class BeverageAdmin(admin.ModelAdmin):
    list_display = ('name','pic','telephone','address','remark')
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'food','beverage','date','expire','finish')
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'bag')
    
admin.site.register(Member, MemberAdmin)
admin.site.register(Savelog, SavelogAdmin)
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Orderlog, OrderlogAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Beverage, BeverageAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Category, CategoryAdmin)


admin.site.register(VehicleBrand)
admin.site.register(VehicleModel)


