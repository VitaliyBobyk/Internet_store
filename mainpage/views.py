from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import Item, Category, UserBasket
from django.core.paginator import Paginator
import re


class BasketView(View):
    def get(self, request):
        if request.user.is_authenticated:
            items_basket = UserBasket.objects.filter(current_user=request.user)
            query_items = []
            for item_basket in items_basket:
                query_items = item_basket.items.all()
            total_price_basket = 0
            for i in query_items:
                total_price_basket += float(i.new_price)
            return query_items, total_price_basket


class ItemsView(BasketView, View):
    def get(self, request):
        items = Item.objects.all()
        items_last = Item.objects.all()[::-2]
        context = {'item_list': items,
                   'item_last': items_last
                   }
        if request.user.is_authenticated:
            basket = BasketView.get(self, request)
            context.setdefault('query_items', basket[0])
            context.setdefault('total_price_basket', basket[1])
        return render(request, "index.html", context)


class About(BasketView, View):
    def get(self, request):
        context = {
        }
        if request.user.is_authenticated:
            basket = BasketView.get(self, request)
            context.setdefault('query_items', basket[0])
            context.setdefault('total_price_basket', basket[1])
        return render(request, "about.html", context)


class Shop(BasketView, View):
    def get(self, request):
        path = re.sub(r'[&]?[?]?page=[0-9]+', '', request.build_absolute_uri())
        category = Category.objects.all()
        one_category = False
        id_category = Category.objects.filter(name__in=request.GET.getlist('category', 'item'))
        category_string = ''
        if 'search' in path:
            items = Item.objects.filter(
                     Q(color__in=request.GET.getlist('color', 'item')) |
                     Q(brand__in=request.GET.getlist('brand', 'item')) |
                     Q(diagonal__in=request.GET.getlist('diagonal', 'item')) |
                     Q(category__in=id_category)
                 )
            one_category = True
            dict_list_category_names = list(id_category.values('name'))
            list_category_names = []
            for item in dict_list_category_names:
                for k, v in item.items():
                    list_category_names.append(v)
            for item in items:
                list_category_names.append(str(item.category))
            category_string = ", ".join(set(list_category_names))
            search_url = '&'
        else:
            items = Item.objects.all()
            search_url = '?'

        colors = Item.objects.values('color').distinct()
        brands = Item.objects.values('brand').distinct()
        diagonals = Item.objects.exclude(diagonal__exact='').values('diagonal').distinct()
        categories = Category.objects.all()

        if 'shop_list' in path:
            paginated_elements = 4
        else:
            paginated_elements = 12

        paginator = Paginator(items, paginated_elements)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        is_paginated = page.has_other_pages()

        if page.has_previous() and one_category == False:
            previous_url = f'?page={page.previous_page_number()}'
        elif page.has_previous() and one_category == True:
            previous_url = f'{path}&page={page.previous_page_number()}'
        else:
            previous_url = ''

        if page.has_next() and one_category == False:
            next_url = f'?page={page.next_page_number()}'
        elif page.has_next() and one_category == True:
            next_url = f'{path}&page={page.next_page_number()}'
        else:
            next_url = ''

        context = {'item_list': page,
                   'category_list': category,
                   'colors': colors,
                   'brands': brands,
                   'diagonals': diagonals,
                   'categories': categories,
                   'one_category': one_category,
                   'category_string': category_string,
                   'is_paginated': is_paginated,
                   'previous_url': previous_url,
                   'next_url': next_url,
                   'search_url': search_url,
                   'path': path
                   }
        if request.user.is_authenticated:
            basket = BasketView.get(self, request)
            context.setdefault('query_items', basket[0])
            context.setdefault('total_price_basket', basket[1])
        if 'shop_list' in path:
            return render(request, "shop_list.html", context)
        else:
            return render(request, "shop.html", context)


class ProductDetail(BasketView, View):
    def get(self, request, pk):
        items = Item.objects.all()
        item = Item.objects.get(id=pk)
        context = {'item_list': items,
                   'item': item
                   }
        if request.user.is_authenticated:
            basket = BasketView.get(self, request)
            context.setdefault('query_items', basket[0])
            context.setdefault('total_price_basket', basket[1])
        return render(request, "product_detail.html", context)


class AddToCart(View):
    def post(self, request):
        if request.user.is_authenticated:
            one_item = Item.objects.filter(id=request.POST.get('wanted_item'))
            obj = UserBasket.objects.get_or_create(current_user=request.user, defaults={'current_user': request.user})
            obj[0].items.add(one_item[0])
            obj[0].save()
        return redirect('/')


class DeleteFromCart(View):
    def post(self, request):
        item_to_delete = Item.objects.filter(id=request.POST.get('item_id'))
        user = UserBasket.objects.get(current_user=request.user)
        user.items.remove(item_to_delete[0])
        user.save()
        return redirect('/')


class ProductCart(BasketView, View):
    def get(self, request):
        if request.user.is_authenticated:
            cart = UserBasket.objects.filter(current_user=request.user)
            items = Item.objects.all()
            context = {
                'user_items': cart[0].items.all(),
                'item_list': items,
            }
            if request.user.is_authenticated:
                basket = BasketView.get(self, request)
                context.setdefault('query_items', basket[0])
                context.setdefault('total_price_basket', basket[1])
            return render(request, 'cart.html', context)
