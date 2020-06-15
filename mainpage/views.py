from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import Item, Category


class ItemsView(View):
    def get(self, request):
        items = Item.objects.all()
        items_last = Item.objects.all()[::-2]
        context = {'item_list': items, 'item_last': items_last}
        return render(request, "index.html", context)


class About(View):
    def get(self, request):
        return render(request, "about.html")


class Shop(View):
    def get(self, request):
        category = Category.objects.all()
        path = request.path
        if 'search' in path:
            items = Item.objects.filter(
                     Q(color__in=request.GET.getlist('color', 'item')) |
                     Q(brand__in=request.GET.getlist('brand', 'item')) |
                     Q(diagonal__in=request.GET.getlist('diagonal', 'item')) |
                     Q(new_price__in=request.GET.getlist('new_price', 'item'))
                 )
        else:
            items = Item.objects.all()

        colors = Item.objects.values('color').distinct()
        brands = Item.objects.values('brand').distinct()
        diagonals = Item.objects.exclude(diagonal__exact='').values('diagonal').distinct()
        prices = Item.objects.values('new_price').distinct()

        context = {'item_list': items, 'category_list': category, 'colors': colors, 'brands': brands,
                   'diagonals': diagonals, 'prices': prices}
        return render(request, "shop.html", context)


class ProductDetail(View):
    def get(self, request, pk):
        items = Item.objects.all()
        item = Item.objects.get(id=pk)
        context = {'item_list': items, 'item': item}
        return render(request, "product_detail.html", context)
