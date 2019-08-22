from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from .models import Product
from .models import Shop, TopCategory, TopSuper, CategoryTag, SuperCategory

# Create your views here.
products = Product.objects.all()
shops = Shop.objects.all()
topcat = TopCategory.objects.all()
topsuper = TopSuper.objects.all()
cattag = CategoryTag.objects.all()
supercat = SuperCategory.objects.all()

n_of_products_one_page = 10
sort_by_products = 0


def categoryview():
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
            # print(j.id)
            print(" printing super category id ")
            # print(j.superCategory)

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

    return top_category_list


def filter_by_category(category):
    if category:
        filtered_products = Product.objects.filter(category__category=category).order_by('name')
    else:
        filtered_products = products
    return filtered_products


def homepage_view(request):
    ctx = {'products_list': products, 'category_list': cattag, 'top_category_list': categoryview()}
    return render(request, "homepage.html", context=ctx)


@csrf_exempt
def ajax_price_filter(request, category):
    filtered_products = filter_by_category(category)

    if request.is_ajax():
        if request.method == 'POST':
            minval = float(request.POST.get('minval', None))
            maxval = float(request.POST.get('maxval', None))
            sortby = request.POST.get('sortby', None).lower()
            shownum = int(request.POST.get('shownumber', None))
            reverselist = (request.POST.get('reverselist', None))
            print("sort by and shownum")
            print(sortby)
            print(shownum)
            print(reverselist)
            filtered_products = filtered_products.filter(price__range=(minval, maxval)).order_by(sortby)
            print("filtered products: ")
            print(filtered_products)
            if reverselist == 'true':
                filtered_products = filtered_products.reverse()
                print('reversed')
                print(filtered_products)

            html = render_to_string(
                template_name="category_page_product_info.html",
                context={'products_list': filtered_products}
            )

            data_dict = {"html_from_view": html}

            return JsonResponse(data=data_dict, safe=False)


def advanced_search(request, category):
    filtered_products = filter_by_category(category)
    print("printing products: ")
    print(filtered_products)
    ctx = {'products_list': filtered_products, 'top_category_list': categoryview()}

    return render(request, "advanced_search.html", context=ctx)


def product_details(request, product_id):
    for product in products:
        if product.id == product_id:
            return render(request, 'product_details.html', {'product_details': product,
                                                            'products_list': products,
                                                            'shops_list': shops})


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


def register_user(request):
    return render(request, 'userreg.html',{})


@login_required
def logout_user(request):
    logout(request)
    msg = "Hope to see you soon! :)"
    messages.add_message(request, messages.INFO, msg)
    return redirect('login_user')
