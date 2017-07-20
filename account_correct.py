from bandongo.models import Savelog,FoodOrder,DrinkOrder
from django.db.models import Sum



save_total = Savelog.objects.all().aggregate(save_total=Sum('money'))['save_total']
foods_total = FoodOrder.objects.filter(finish=True).aggregate(foods_total=Sum('price'))['foods_total']
drinks_total = DrinkOrder.objects.filter(finish=True).aggregate(drinks_total=Sum('price'))['drinks_total']
if foods_total == None:
	foods_total = 0
if drinks_total == None:
	drinks_total = 0
cost_total = foods_total + drinks_total
total_sum = save_total - cost_total
print total_sum

members=Member.objects.all()
for m in members:
	allSavings=Savelog.objects.filter(memberName=m).aggregate(save_total=Sum('money'))['save_total']
	if allSavings == None:
		allSavings = 0
	foods_total = FoodOrder.objects.filter(memberName=m,finish=True).aggregate(foods_total=Sum('price'))['foods_total']
	drinks_total = DrinkOrder.objects.filter(memberName=m,finish=True).aggregate(drinks_total=Sum('price'))['drinks_total']
	if foods_total == None:
		foods_total = 0
	if drinks_total == None:
		drinks_total = 0
	allSpend=foods_total+drinks_total
	
	fakeBalance=allSavings-allSpend
	trueBalance=m.saving
	
	mad=Member.objects.get(pk=17)
	Savelog.objects.create(memberName=m, money=trueBalance-fakeBalance, adminName=mad, comment="修正餘額錯誤")