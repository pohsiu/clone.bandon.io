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