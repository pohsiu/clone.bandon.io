from bandongo.models import Member,Savelog,FoodOrder,DrinkOrder
from django.db.models import Sum

toDo = Member.objects.filter(remark__name='替代役')

for i in toDo:
	save_total = Savelog.objects.filter(memberName=i.id).aggregate(save_total=Sum('money'))['save_total']
	foods_total = FoodOrder.objects.filter(memberName=i.id,finish=True).aggregate(foods_total=Sum('price'))['foods_total']
	drinks_total = DrinkOrder.objects.filter(memberName=i.id,finish=True).aggregate(drinks_total=Sum('price'))['drinks_total']
	if foods_total == None:
		foods_total = 0
	if drinks_total == None:
		drinks_total = 0
	cost_total = foods_total + drinks_total
	total_sum = save_total - cost_total
	Member.objects.filter(id=i.id).update(saving=total_sum)