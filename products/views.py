from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Product
from .models import Shop
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import ShopProduct
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.urls import reverse

# Create your views here.
products = Product.objects.all()
shops = Shop.objects.all()
n_of_products_one_page = 10
sort_by_products = 0


def index(request):
    return render(request, 'index.html', {'products_list': products})



def advanced_search(request):
    sort_by = 0
    n_products = 10
    filter_price = "nothing"
    min_filter_price = 0
    max_filter_price = 10000
    location_filter = 1
    if request.method == 'GET':
        if request.GET.get('id_sort') is not None:
            sort_by = int(request.GET.get('id_sort'))

        if request.GET.get('n_products') is not None:
            n_products = int(request.GET.get('n_products'))
        print("checking")
        p2 = request.GET.get('max-price-filter')
        p1 = request.GET.get('min-price-filter')
        p3 = request.GET.get('location-filter')
        if p1 is not None and p1 != '':
            print("invalid")
            min_filter_price = int(p1, 10)

        if p2 is not None and p2 != '':
            max_filter_price = int(p2, 10)

        if p3 is not None and p3 != '':
            location_filter = int(p3, 10)

        print("sort by :")
        print(sort_by)
        print(n_products)
        print(filter_price)
        print(location_filter)
    trimmed_products = products
    if sort_by == 2:
        print("dhukse sort er vitor")
        trimmed_products = trimmed_products.order_by('rating')
    elif sort_by == 1:
        trimmed_products = trimmed_products.order_by('price')
    filtered_products = []
    for p in trimmed_products:
        if ((p.price >= min_filter_price) and (p.price <= max_filter_price)):
            filtered_products.append(p)

    return render(request, 'advanced_search.html',
                  {'products_list': filtered_products, 'shops_list': shops, 'products_one_page': n_products, })


def product_details(request, product_id):
    for product in products:
        if product.id == product_id:
            return render(request, 'product_details.html', {'product_details': product,
                                                            'products_list': products,
                                                            'shops_list': shops})


def initial_page(request):
    return render(request, 'homepage.html', {'products_list': products, 'shops_list': shops})

def validate_user(request, username, email):
    try:
        user = User.objects.get(Q(username=username) | Q(email=email))
    except User.DoesNotExist:
        user = None

    if user is not None:
        # user already exists
        return True
    else:
        return False

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Welcome back!')
            return render(request, 'homepage.html', {'products_list': products, 'shops_list': shops})
        else:
            messages.add_message(request, messages.ERROR, 'Invalid login')
            return render(request, 'userlogin.html', {
                'view': 'login',
            })
    else:
        return render(request, 'userlogin.html', {
            'view': 'login',
        })


@login_required
def logout_user(request):
    logout(request)
    msg = "Hope to see you soon! :)"
    messages.add_message(request, messages.INFO, msg)
    return redirect('login_user')
