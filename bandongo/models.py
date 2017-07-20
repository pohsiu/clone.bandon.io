from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User


BAGS=[(1, 1), (2, 2), (3, 3)]

#category
class Category(models.Model):
    name = models.CharField(max_length=10)
    bag = models.IntegerField(choices=BAGS)
    def __unicode__(self):
        return u'%s '% (self.name)


#basic informations
class Member(models.Model):
    name = models.CharField(max_length=10)
    #password = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, verbose_name='e-mail')
    remark = models.ForeignKey(Category)
    auth = models.CharField(max_length=10, default='normal')
    saving = models.IntegerField(default=0)
    lineid = models.CharField(max_length=100, default='')
    
    def store(self):
        self.save()
    def __unicode__(self):
        return u'%s' % (self.name)
        
    
    
#Saving record
class Savelog(models.Model):
    memberName = models.ForeignKey(Member, related_name='person') # not sure can operate
    money = models.IntegerField()
    tranDate = models.DateTimeField(default=timezone.now)
    adminName = models.ForeignKey(Member, default=None, related_name='admin', null=True, on_delete=models.SET_NULL,)
    comment = models.CharField(max_length=50, blank=True)
    def __unicode__(self):
        return u'%s' % (self.memberName)
    

#Shop information
class Food(models.Model):
    name = models.CharField(max_length=15)
    pic = models.ImageField(upload_to="static/pic/food/",blank=True) #shop picture loading path
    telephone = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    remark = models.CharField(max_length=15,blank=True)
    
    
    def __unicode__(self):
        return u'%s '% (self.name)
 
class Drink(models.Model):
    name = models.CharField(max_length=15)
    pic = models.ImageField(upload_to="static/pic/catalogPic/",blank=True)
    telephone = models.CharField(max_length=15)
    address =models.CharField(max_length=50)
    remark = models.CharField(max_length=15,blank=True)
    
    def __unicode__(self):
        return u'%s '% (self.name)

#Product Food Menu
class Catalog(models.Model):
    foodShop = models.ForeignKey(Food)
    name = models.CharField(max_length=15)
    pic = models.ImageField(upload_to="static/pic/catalogPic/",blank=True)
    price = models.IntegerField()
    
    def store(self):
        self.save()
    def __unicode__(self):
        return u'%s '% (self.name)

class Schedule(models.Model):
    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=50, blank=True)
    food = models.ForeignKey(Food)
    catalogs = models.ManyToManyField(Catalog)
    drink = models.ForeignKey(Drink, blank=True)
    date = models.DateTimeField() 
    expire = models.BooleanField(default=False)
    foodArrived = models.BooleanField(default=False)
    drinkArrived = models.BooleanField(default=False)
    finish = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'%s'% (self.name)

#Transaction log
class FoodOrder(models.Model):
    memberName = models.ForeignKey(Member)
    scheduleName = models.ForeignKey(Schedule)
    foodName = models.ForeignKey(Catalog)
    num = models.IntegerField(default=1) #single product ordering num 
    date = models.DateTimeField(default=timezone.now)
    remark = models.CharField(max_length=20,blank=True)
    price = models.IntegerField(default=0)
    finish = models.BooleanField(default=False)
    
    def store(self):
        self.save()
    def __unicode__(self):
        return u'%s '% (self.memberName)

class DrinkOrder(models.Model):
    memberName = models.ForeignKey(Member)
    scheduleName = models.ForeignKey(Schedule)
    drinking = models.CharField(max_length=15)
    num = models.IntegerField(default=1) #single product ordering num 
    date = models.DateTimeField(default=timezone.now)
    remark = models.CharField(max_length=20,blank=True)
    price = models.IntegerField(default=0)
    finish = models.BooleanField(default=False)
    
    
    def store(self):
        self.save()
    def __unicode__(self):
        return u'%s '% (self.memberName)
        
class Notification(models.Model):
    classification = models.IntegerField()
    # 1: no savings
    # 2: messages
    subject = models.ForeignKey(Member)
    content = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    
    
    def store(self):
        self.save()
    def __unicode__(self):
        return u'%s '% (self.content)
        
class Message(models.Model):
    # id
    # 1: homeMessage
    # 2: greetingMessage
    usage = models.CharField(max_length=50)
    content = models.TextField()
    def store(self):
        self.save()
    def __unicode__(self):
        return u'%s '% (self.content)
        

class WishFood(models.Model):
    member = models.ForeignKey(Member)
    food = models.ForeignKey(Food)
    date = models.DateField(default=timezone.now)
    realized = models.BooleanField(default=False)
    def __unicode__(self):
        return u'%s '% (self.food)
    
class WishDrink(models.Model):
    member = models.ForeignKey(Member)
    drink = models.ForeignKey(Drink)
    date = models.DateField(default=timezone.now)
    realized = models.BooleanField(default=False)
    def __unicode__(self):
        return u'%s '% (self.drink)
    