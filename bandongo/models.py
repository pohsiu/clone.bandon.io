from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User




#category
class Category(models.Model):
    category_name = models.CharField(max_length=10)
    
    def __unicode__(self):
        return u'%s '% (self.category_name)


#basic informations
class Member(models.Model):
    name = models.CharField(max_length=10)
    #password = models.CharField(max_length=50)
    member_phone = models.CharField(max_length=15)
    member_email = models.EmailField(blank=True, verbose_name='e-mail')
    member_mark = models.ForeignKey(Category)
    # member_mark = models.CharField(max_length=10, blank=True)
    member_auth = models.CharField(max_length=10, default='normal')
    member_saving = models.IntegerField(default=0)
    
    def store(self):
        self.save()
    def __unicode__(self):
        return u'%s' % (self.name)
        
    # def __str__(self):
    #     return self.name
    
#Saving record
class Savelog(models.Model):
    member_name = models.ForeignKey(Member, related_name='person') # not sure can operate
    money = models.IntegerField()
    tran_date = models.DateTimeField(default=timezone.now)
    admin_name = models.ForeignKey(Member, default='none', related_name='admin')
    def __unicode__(self):
        return u'%s' % (self.member_name)
    

#Shop information
class Shop(models.Model):
    name = models.CharField(max_length=10)
    pic = models.URLField(blank=True) #shop picture loading path
    telephone = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    remark = models.CharField(max_length=15,blank=True)
    
    
    def __unicode__(self):
        return u'%s '% (self.name)
 
class Beverage(models.Model):
    name = models.CharField(max_length=10)
    pic = models.URLField(blank=True)
    telephone = models.CharField(max_length=15)
    address =models.CharField(max_length=50)
    remark = models.CharField(max_length=15,blank=True)
    
    def __unicode__(self):
        return u'%s '% (self.name)

class Schedule(models.Model):
    name = models.CharField(max_length=15)
    comment = models.CharField(max_length=50, blank=True)
    food = models.ForeignKey(Shop)
    beverage = models.ForeignKey(Beverage, blank=True)
    date = models.DateTimeField() 
    expire = models.BooleanField(default=False)
    finish = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'%s'% (self.name)
   
#Product Food Menu
class Catalog(models.Model):
    shop_name = models.ForeignKey(Shop)
    name = models.CharField(max_length=10)
    pic = models.URLField(blank=True)
    price = models.IntegerField()
    
    def store(self):
        self.save()
    def __unicode__(self):
        return u'%s '% (self.name)
        



#Transaction log
class Orderlog(models.Model):
    member_name = models.ForeignKey(Member)
    schedule_name = models.ForeignKey(Schedule)
    catalog_name = models.CharField(max_length=10)
    ordernum = models.IntegerField(default=1) #single product ordering num 
    orderdate = models.DateTimeField(default=timezone.now)
    orderremark = models.CharField(max_length=10,blank=True)
    orderprice = models.IntegerField(default=0)
    
    
    
    def __unicode__(self):
        return u'%s '% (self.member_name)
        
        

        
#testing code
class VehicleBrand(models.Model):
    description = models.CharField(max_length=100)
    code = models.SlugField(primary_key=True)

class VehicleModel(models.Model):
    description = models.CharField(max_length=100)
    code = models.SlugField(primary_key=True)
    brand = models.ForeignKey(VehicleBrand)
