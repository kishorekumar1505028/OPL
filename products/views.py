from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from .models import Product
from .models import Shop, TopCategory, TopSuper, CategoryTag, SuperCategory
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


def categoryview(request):
    topcat = TopCategory.objects.all()
    topsuper = TopSuper.objects.all()
    cattag = CategoryTag.objects.all()
    supercat = SuperCategory.objects.all()

    top_category_list = []

    for i in topcat:
        tempsuper = topsuper.filter(topCategory_id=i.id)

        print("\n i's id (top category id) ")
        print(i.id)
        print(i.topCategory)
        print(" printing super category list")
        print(tempsuper)

        super_category_list = []

        for j in tempsuper:

            print("\nj's id ")
            print(j.id)
            print(" printing super category id ")
            print(j.superCategory)

            super_category_object = supercat.filter(id=j.superCategory_id)
            category_list = (cattag.filter(superCategory_id=j.superCategory_id))

            for oj in super_category_object:
                super_category_name = oj.superCategory
            category_name_list = []
            for oj in category_list:
                category_name_list.append(oj.category)

            super_category_dictionary = {
                'super_category': super_category_name,
                'category_list': category_name_list
            }
            super_category_list.append(super_category_dictionary)

        top_category_dictionary = {
            'top_category': i.topCategory,
            'super_category_list': super_category_list
        }

        top_category_list.append(top_category_dictionary)
        print("printing added dictionary")
        print(top_category_dictionary)

    print(top_category_list)
    return render(request, 'homepage.html',
                  {'products_list': products, 'top_category_list': top_category_list})


def television_filter(taglist):
    return 0


def index(request):
    return render(request, 'index.html', {'products_list': products})


def advanced_search(request):
    if request.method == 'GET':
        req_category = request.GET.get('category', None)
        filtered_products = serializers.serialize('json', Product.objects.filter(category__category=req_category))
        data = {
            'product_list': filtered_products
        }
    return JsonResponse(data)


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
