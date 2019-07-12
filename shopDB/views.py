from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from products.models import User, Product, Shop
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

# Create your views here.

log_stat = 0
log_user = None

def All_products_view(request):
    products = Product.objects.all().order_by('-rating')
    return render(request, 'view_prod_list.html', {'products_list': products})

    #return render(request, 'index.html', {'products_list': products})



def login_view_s(request):
    # print (request.POST.get('username'))
    users = User.objects.all()
    shops = Shop.objects.all()
    if request.method == 'POST':
        print(request.POST.get('username'))
        print ('POST method called')
        user = request.POST.get('username')
        passwd = request.POST.get('psw')

        for u in users:
            if user == u.name and passwd == '12345':
                print ('user found')
                for shop in shops:
                    if shop.owner_id == u.iduser:
                        print ('shop found')
                        log_stat  = 1
                        print ('log stat turned 1')
                        #login(request, u)
                        log_user = u
                        return render(request, 'shopHome.html', {'User': u, 'Shop': shop})

                return render(request, 'noShop_error.html')
        #log_stat = 0
        return render(request, 'error.html')
    else:
        log_stat = 0
        print ('log stat turned 0')
        return render(request, 'login_shop.html')



def login_success_view(request):
    users = User.objects.all()
    shops = Shop.objects.all()
    for u in users:
        if u.name == 'sagor':
            for shop in shops:
                if shop.owner == u.iduser:
                    return render(request, 'shopHome.html', {'User': u, 'Shop': shop})

    us = User.objects.filter(name='sagor')
    sp = Shop.objects.filter(location='nilkhet')
    return render(request, 'shopHome.html', {'User': us, 'Shop': sp})




def logout_view(request):
    log_user = None
    return render(request, 'login_shop.html')


def user_view(request):
    return render(request,'user_home.html')


def product_detail(request, slug):
    products = Product.objects.all()
    for prod in products:
        if prod.productname == slug:
            break

    return render(request,'product_detail.html',{'product':prod})


    #pr = Product.objects.filter(id==1)
    #return render(request,'product_detail.html',{'product':pr})