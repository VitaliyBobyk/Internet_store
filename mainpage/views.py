from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import Item, Category, UserBasket,UserReviews
from django.core.paginator import Paginator
from .forms import ReviewForm
import re


class BasketView(View):
    def get(self, request):
        """Отримання корзини конкретного користувача"""
        if request.user.is_authenticated:
            items_basket = UserBasket.objects.filter(current_user=request.user)
            query_items = []
            for item_basket in items_basket:
                query_items = item_basket.items.all()
            total_price_basket = 0
            for i in query_items:
                total_price_basket += float(i.new_price)
            return query_items, total_price_basket


def user_basket_items(request, context):
    """Отриманні предметів котрі знаходяться в корзині користувача"""
    basket = BasketView.get(..., request)
    context.setdefault('query_items', basket[0])
    context.setdefault('total_price_basket', basket[1])
    return context


class ItemsView(View):
    """Рендер головної сторінки з товарами"""
    def get(self, request):
        items = Item.objects.all()
        items_last = Item.objects.all()[::-2]
        context = {'item_list': items,
                   'item_last': items_last
                   }
        if request.user.is_authenticated:
            user_basket_items(request, context)
        return render(request, "index.html", context)


class About(View):
    """Рендер сторінки про магазин"""
    def get(self, request):
        context = {
        }
        if request.user.is_authenticated:
            user_basket_items(request, context)
        return render(request, "about.html", context)


def search(request):
    """Реалізація можливості пошуку товару за фільтром"""
    path = re.sub(r'[&]?[?]?page=[0-9]+', '', request.build_absolute_uri())
    category = Category.objects.all()
    id_category = Category.objects.filter(name__in=request.GET.getlist('category', 'item'))
    one_category = False
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
    return {'path': path, 'category': category, 'items': items, 'one_category': one_category, 'category_string': category_string, 'search_url': search_url}


def db_getting_items():
    """Отримання з бази данних категорій за якими сотруються елементи"""
    colors = Item.objects.values('color').distinct()
    brands = Item.objects.values('brand').distinct()
    diagonals = Item.objects.exclude(diagonal__exact='').values('diagonal').distinct()
    categories = Category.objects.all()
    return {'colors': colors, 'brands': brands, 'diagonals': diagonals, 'categories': categories}


def pagination(request, path, items, one_category):
    """Створення пагінації сторінок"""
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
    return {'page': page, 'is_paginated': is_paginated, 'previous_url': previous_url, 'next_url': next_url}


class Shop(View):
    """Рендер сторінки з товарами та фільтрацією товарів"""
    def get(self, request):
        search_items = search(request)
        get_database_items = db_getting_items()
        pagination_page = pagination(request, search_items['path'], search_items['items'], search_items["one_category"])

        context = {'item_list': pagination_page['page'],
                   'category_list': search_items["category"],
                   'colors': get_database_items['colors'],
                   'brands': get_database_items['brands'],
                   'diagonals': get_database_items['diagonals'],
                   'categories': get_database_items['categories'],
                   'one_category': search_items["one_category"],
                   'category_string': search_items["category_string"],
                   'is_paginated': pagination_page['is_paginated'],
                   'previous_url': pagination_page['previous_url'],
                   'next_url': pagination_page['next_url'],
                   'search_url': search_items["search_url"],
                   'path': search_items['path']
                   }
        if request.user.is_authenticated:
            user_basket_items(request, context)
        if 'shop_list' in search_items['path']:
            return render(request, "shop_list.html", context)
        else:
            return render(request, "shop.html", context)


class ProductDetail(View):
    """Рендер головної сторінки з деталями про один товар"""
    def post(self, request, pk):
        """Реалізація можливості відгуку користувача на кокретну позицію товару"""
        item = Item.objects.get(id=pk)
        if request.user.is_authenticated:
            if request.method == 'POST':
                form = ReviewForm(request.POST)
                if form.is_valid() or None:
                    """Запис нового поста в БД"""
                    review = form.save(commit=False)
                    review.current_user = request.user
                    review.item = item
                    review.reting = request.POST.get('rating')
                    review.save()
                    return redirect(f'http://127.0.0.1:8000/product_detail/{pk}')

    def get(self, request, pk):
        """Реалізація можливості перегляду відгуків користувачів на коткретну позицію товару"""
        items = Item.objects.all()
        item = Item.objects.get(id=pk)
        form = ReviewForm()
        reviews = UserReviews.objects.filter(item=item)
        context = {'item_list': items,
                   'item': item,
                   'reviews': reviews,
                   'form': form,
                   }

        if request.user.is_authenticated:
            user_basket_items(request, context)
        return render(request, "product_detail.html", context)


class AddToCart(View):
    """Реалізація можливості додавання товару в корзину"""
    def post(self, request):
        if request.user.is_authenticated:
            one_item = Item.objects.filter(id=request.POST.get('wanted_item'))
            obj = UserBasket.objects.get_or_create(current_user=request.user, defaults={'current_user': request.user})
            obj[0].items.add(one_item[0])
            obj[0].save()
        return redirect('/')


class DeleteFromCart(View):
    """Реалізація можливості видалення товару з корзини"""
    def post(self, request):
        item_to_delete = Item.objects.filter(id=request.POST.get('item_id'))
        user = UserBasket.objects.get(current_user=request.user)
        user.items.remove(item_to_delete[0])
        user.save()
        return redirect('/')


class ProductCart(View):
    """Реалізація можливості перегляду корзини користувача"""
    def get(self, request):
        if request.user.is_authenticated:
            cart = UserBasket.objects.filter(current_user=request.user)
            items = Item.objects.all()
            context = {
                'user_items': cart[0].items.all(),
                'item_list': items,
            }
            if request.user.is_authenticated:
                user_basket_items(request, context)
            return render(request, 'cart.html', context)


class SearchProducts(View):
    """Реалізація можливості пошуку товару"""
    def get(self, request):
        items = Item.objects.filter(
            Q(title__icontains=request.GET.get('filter')) |
            Q(brand__icontains=request.GET.get('filter'))
        )
        items_last = Item.objects.all()[::-2]
        context = {'item_list': items,
                   'item_last': items_last
                   }
        if request.user.is_authenticated:
            user_basket_items(request, context)
        return render(request, "index.html", context)

