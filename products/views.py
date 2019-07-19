from django.http import HttpResponse
from django.shortcuts import render
from .models import Product
from .models import User
from .models import Shop
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.urls import reverse


# Create your views here.


def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products_list': products})

def user_login(request):
    return render(request, 'userlogin.html')

def product_details(request):
    products = Product.objects.all()
    shops = Shop.objects.all()
    return render(request, 'product_details.html' , {'products_list': products, 'shops_list': shops})


def initial_page(request):
    products = Product.objects.all()
    shops = Shop.objects.all()
    return render(request, 'homepage.html', {'products_list': products, 'shops_list': shops})


def login_view(request):
    # print('hello')
    # print (request.POST.get('username'))
    # return HttpResponse("Hello, world. You're at the login.")
    flag = 0
    users = User.objects.all()
    if request.method == 'POST':
        print(request.POST.get('username'))
        user = request.POST.get('username')
        passwd = request.POST.get('psw')

        for u in users:
            if user == u.name and passwd == '12345':
                products = Product.objects.all();
                return render(request, 'homepage.html', {'products_list': products})

        return render(request, 'error.html')
    else:
        return render(request, 'login.html')
