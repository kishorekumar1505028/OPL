from django.http import HttpResponse
from django.shortcuts import render
from .models import Product
from .models import User
from .models import Shop
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.urls import reverse

# Create your views here.
products = Product.objects.all()
aproducts = Product.objects.all()
shops = Shop.objects.all()
n_of_products_one_page = 10
sort_by_products = 0


def index(request):
    return render(request, 'index.html', {'products_list': products})


def user_login(request):
    return render(request, 'userlogin.html')


def advanced_search(request, n_products, sort_criteria):
    trimmed_products = aproducts
    if sort_criteria == 2:
        trimmed_products = trimmed_products.order_by('rating')
    elif sort_criteria == 1:
        trimmed_products = trimmed_products.order_by('price')
    if n_products != 5:
        n_of_products_one_page = n_products
    else :
        n_of_products_one_page = 10

    aproducts = trimmed_products


    return render(request, 'advanced_search.html',
              {'products_list': trimmed_products, 'shops_list': shops, 'products_one_page': n_of_products_one_page,
               'sort_by': sort_by_products, })


def product_details(request, product_id):
    for product in products:
        if product.idproduct == product_id:
            return render(request, 'product_details.html', {'product_details': product,
                                                            'products_list': products,
                                                            'shops_list': shops})


def initial_page(request):
    return render(request, 'homepage.html', {'products_list': products, 'shops_list': shops})
