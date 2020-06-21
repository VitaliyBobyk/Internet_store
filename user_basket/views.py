from django.shortcuts import render
from django.views.generic.base import View
from .models import *


class BasketView(View):
    def get(self, request):
        if request.user.is_authenticated:
            pass
        items_basket = UserBasket.objects.filter(current_user=request.user)
        query_items = []
        for item_basket in items_basket:
            query_items = item_basket.items.all()
        total_price_basket = 0
        for i in query_items:
            total_price_basket += int(i.new_price)
        print(total_price_basket)
        context = {'query_items': query_items, 'total_price_basket': total_price_basket}
        return render(request, "user_basket.html", context)
