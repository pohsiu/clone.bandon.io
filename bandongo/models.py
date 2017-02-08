from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User




#category
class Category(models.Model):
    name = models.CharField(max_length=10)
    bag = models.IntegerField()
    def __unicode__(self):
        return u'%s '% (self.name)


#basic informations
class Member(models.Model):
    name = models.CharField(max_length=10)
    #password = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, verbose_name='e-mail')
    remark = models.ForeignKey(Category)
    # member_mark = models.CharField(max_length=10, blank=True)
    auth = models.CharField(max_length=10, default='normal')
    saving = models.IntegerField(default=0)
    
    def store(self):
        self.save()
    def __unicode__(self):
        return u'%s' % (self.name)
        
    # def __str__(self):
    #     return self.name
    
#Saving record
class Savelog(models.Model):
    memberName = models.ForeignKey(Member, related_name='person') # not sure can operate
    money = models.IntegerField()
    tranDate = models.DateTimeField(default=timezone.now)
    adminName = models.ForeignKey(Member, default='none', related_name='admin')
    comment = models.CharField(max_length=50, blank=True)
    def __unicode__(self):
        return u'%s' % (self.memberName)
    

#Shop information
class Food(models.Model):
    name = models.CharField(max_length=10)
    pic = models.URLField(blank=True) #shop picture loading path
    telephone = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    remark = models.CharField(max_length=15,blank=True)
    
    
    def __unicode__(self):
        return u'%s '% (self.name)
 
class Drink(models.Model):
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
    food = models.ForeignKey(Food)
    drink = models.ForeignKey(Drink, blank=True)
    date = models.DateTimeField() 
    expire = models.BooleanField(default=False)
    finish = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'%s'% (self.name)
   
#Product Food Menu
class Catalog(models.Model):
    foodShop = models.ForeignKey(Food)
    name = models.CharField(max_length=10)
    pic = models.URLField(blank=True)
    price = models.IntegerField()
    choosed = models.BooleanField(default=False)
    
    def store(self):
        self.save()
    def __unicode__(self):
        return u'%s '% (self.name)
        



#Transaction log
class FoodOrder(models.Model):
    memberName = models.ForeignKey(Member)
    scheduleName = models.ForeignKey(Schedule)
    foodName = models.ForeignKey(Catalog)
    num = models.IntegerField(default=1) #single product ordering num 
    date = models.DateTimeField(default=timezone.now)
    remark = models.CharField(max_length=10,blank=True)
    price = models.IntegerField(default=0)
    
    
    def store(self):
        self.save()
    def __unicode__(self):
        return u'%s '% (self.memberName)

class DrinkOrder(models.Model):
    memberName = models.ForeignKey(Member)
    scheduleName = models.ForeignKey(Schedule)
    drinking = models.CharField(max_length=10)
    num = models.IntegerField(default=1) #single product ordering num 
    date = models.DateTimeField(default=timezone.now)
    remark = models.CharField(max_length=10,blank=True)
    price = models.IntegerField(default=0)
    
    
    def store(self):
        self.save()
    def __unicode__(self):
        return u'%s '% (self.memberName)
        
        

        

