from django.http import HttpResponse
from django.shortcuts import render
from .models import Product
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login


# Create your views here.


def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products_list': products})

def initial_page(request):
    products = Product.objects.all()
    return render(request, 'initialpage.html', {'products_list': products})


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
                products = Product.objects.all() ;
                return render(request, 'initialpage.html', {'products_list': products})

        return render(request, 'error.html')
    else:
        return render(request, 'login.html')
