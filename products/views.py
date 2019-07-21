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
shops = Shop.objects.all()


def index(request):
    return render(request, 'index.html', {'products_list': products})


def user_login(request):
    return render(request, 'userlogin.html')

def advanced_search(request):
    return render(request, 'advanced_search.html',{'products_list': products, 'shops_list': shops})


def product_details(request, product_id):

    for product in products:
        if product.idproduct == product_id:
            return render(request, 'product_details.html', {'product_details': product,
                                                            'products_list': products,
                                                            'shops_list': shops})
def initial_page(request):
    return render(request, 'homepage.html', {'products_list': products, 'shops_list': shops})


