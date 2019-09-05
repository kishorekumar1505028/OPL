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
from django.http import HttpResponseRedirect

from products.models import Cart, WishList
from .models import Product
from .models import Shop, TopCategory, TopSuper, CategoryTag, SuperCategory, ProductReview

# Create your views here.
products = Product.objects.all()
shops = Shop.objects.all()
topcat = TopCategory.objects.all()
topsuper = TopSuper.objects.all()
cattag = CategoryTag.objects.all()
supercat = SuperCategory.objects.all()
product_reviews = ProductReview.objects.all()

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


def get_category_data():
    category_data = {'category_list': cattag,
                     'top_category_list': categoryview()}
    return category_data


def get_user_cart(request):
    if request.user.is_authenticated:
        print("in get_user_cart function user is authenticated")
        print(request.user.id)
        user_cart = Cart.objects.all().filter(user__id=request.user.id)
        return user_cart
    else:
        return []


def get_user_cart_session(request):
    if "user_cart" in request.session:
        return request.session['user_cart']
    else:
        return []


def get_owner_cart(request):
    if request.user.is_authenticated:
        print("in get_owner_cart function user is authenticated")
        print(request.user.id)
        user_cart = Cart.objects.all().filter(product__owner_id=request.user.id)
        return user_cart
    else:
        return []


def get_user_wishlist(request):
    if request.user.is_authenticated:
        print("in get_user_wishlist function user is authenticated")
        print(request.user.id)
        user_wishlist = WishList.objects.all().filter(user__id=request.user.id)
        return user_wishlist
    else:
        return []


def get_cart_size(request):
    user_cart = get_user_cart(request)
    if user_cart is None:
        return 0
    else:
        total = 0
        for p in user_cart:
            total += p.quantity
        return total


def get_homepage_header_data(request):
    homepage_header_info = {'user_cart': get_user_cart(request), 'cart_size': get_cart_size(request)}
    return homepage_header_info


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


@csrf_exempt
def add_to_cart(request):
    data_dict = {}
    if request.user.is_authenticated:

        given_id = int(request.POST.get('product_id'))
        qty = int(request.POST.get('numbers'))
        cart_product = products.filter(id=given_id)
        particular_user_product = Cart.objects.all().filter(user__id=request.user.id,
                                                            product_id=given_id)
        if cart_product.first() is None:
            data_dict['error_msg'] = "Product not found"

        elif cart_product.first().quantity < qty:
            data_dict['error_msg'] = "Product not available"

        print(particular_user_product)
        if particular_user_product:
            new_quantity = particular_user_product.first().quantity + qty
            particular_user_product.update(quantity=new_quantity)
            newq = cart_product.first().quantity - qty
            cart_product.update(quantity=newq)
            print(particular_user_product)
        else:
            print("creating..")
            Cart.objects.create(user_id=request.user.id, product_id=given_id, quantity=qty)

        print("getting user cart")
        user_cart = get_user_cart(request)
        for rows in user_cart:
            print(rows.product.name)

        html = render_to_string(
            template_name="small_cart.html",
            context={'user_cart': get_user_cart(request)}
        )

        cart_size_html = render_to_string(
            template_name="cart_size.html",
            context={'cart_size': get_cart_size(request)}
        )

        print("printing html")
        print(html)
        print("printing cart size html")
        print(cart_size_html)

        data_dict['html_from_view'] = html
        data_dict['html_cart_size'] = cart_size_html

    else:
        data_dict['error_msg'] = "Please login or register first"

    return JsonResponse(data=data_dict, safe=False)


def add_to_cart(request):
    data_dict = {}
    if request.user.is_authenticated:

        given_id = int(request.POST.get('product_id'))
        qty = int(request.POST.get('numbers'))
        cart_product = products.filter(id=given_id)
        particular_user_product = Cart.objects.all().filter(user__id=request.user.id,
                                                            product_id=given_id)
        new_quantity = particular_user_product.first().quantity + qty
        if cart_product.first() is None:
            data_dict['error_msg'] = "Product not found"

        elif new_quantity < qty:
            data_dict['error_msg'] = "Product not available"

        #print(particular_user_product)
        elif particular_user_product:

            particular_user_product.update(quantity=new_quantity)
            #newq = cart_product.first().quantity - qty
            #cart_product.update(quantity=newq)
            print(particular_user_product)
    else:
        print("creating..")
        Cart.objects.create(user_id=request.user.id, product_id=given_id, quantity=qty)

    print("getting user cart")
    user_cart = get_user_cart(request)
    for rows in user_cart:
        print(rows.product.name)

    html = render_to_string(
        template_name="small_cart.html",
        context={'user_cart': get_user_cart(request)}
    )

    cart_size_html = render_to_string(
        template_name="cart_size.html",
        context={'cart_size': get_cart_size(request)}
    )

    print("printing html")
    print(html)
    print("printing cart size html")
    print(cart_size_html)

    data_dict['html_from_view'] = html
    data_dict['html_cart_size'] = cart_size_html

else:
data_dict['error_msg'] = "Please login or register first"

return JsonResponse(data=data_dict, safe=False)


@csrf_exempt
def add_to_wishlist(request):
    data_dict = {}
    if request.user.is_authenticated:

        given_id = int(request.POST.get('product_id'))
        wishlist_product = products.filter(id=given_id)
        particular_user_product = WishList.objects.all().filter(user__id=request.user.id,
                                                                product_id=given_id)
        if wishlist_product.first() is None:
            data_dict['error_msg'] = "Product not found"

        print(particular_user_product)
        if particular_user_product:
            data_dict['error_msg'] = "Product is already added to wishlist"
        else:
            print("creating..")
            WishList.objects.create(user_id=request.user.id, product_id=given_id, quantity=1)

        print("getting user wishlist")
        user_wishlist = get_user_wishlist(request)
        for rows in user_wishlist:
            print(rows.product.name)

        html = render_to_string(
            template_name="wishlist_info.html",
            context={'user_wishlist': get_user_wishlist(request)}
        )

        cart_size_html = render_to_string(
            template_name="cart_size.html",
            context={'cart_size': get_cart_size(request)}
        )

        print("printing cart size html")
        print(cart_size_html)
        data_dict['html_from_view'] = html
        data_dict['html_cart_size'] = cart_size_html

    else:
        data_dict['error_msg'] = "Please login or register first"

    return JsonResponse(data=data_dict, safe=False)


@csrf_exempt
def homepage_view(request):
    if request.is_ajax():
        act = request.POST.get('act')
        if act == 'add_to_cart':
            return add_to_cart(request)
        elif act == 'add_to_wishlist':
            return add_to_wishlist(request)

    else:

        homepage_header_data = get_homepage_header_data(request)
        category_data = get_category_data()
        products_dict = {'products_list': products}
        ctx = {}
        ctx.update(homepage_header_data)
        ctx.update(category_data)
        ctx.update(products_dict)
        return render(request, "homepage.html", context=ctx)


@csrf_exempt
def advanced_search(request, category):
    if request.is_ajax():
        act = request.POST.get('act')
        if act == 'add_to_cart':
            return add_to_cart(request)
        elif act == 'add_to_wishlist':
            return add_to_wishlist(request)

    else:

        filtered_products = filter_by_category(category)
        print("printing products: ")
        print(filtered_products)
        ctx = {'products_list': filtered_products, 'top_category_list': categoryview(),
               'user_cart': get_user_cart(request),
               'cart_size': get_cart_size(request)}

        return render(request, "advanced_search.html", context=ctx)


def cart_details(request):
    return render(request, "cart.html", {'top_category_list': categoryview(), 'user_cart': get_user_cart(request),
                                         'cart_size': get_cart_size(request)})


def order_request_details(request):
    return render(request, "order_request.html",
                  {'top_category_list': categoryview(), 'user_cart': get_owner_cart(request),
                   'cart_size': get_cart_size(request)})


def wishlist_details(request):
    return render(request, "wishlist.html",
                  {'top_category_list': categoryview(), 'user_wishlist': get_user_wishlist(request),
                   'cart_size': get_cart_size(request)})


@csrf_exempt
def place_order(request):
    data_dict = {}
    if request.user.is_authenticated:
        user_cart = get_user_cart(request)
        user_cart.delete()
    else:
        data_dict['error_msg'] = 'Placing order failed'

    html = render_to_string(
        template_name="cart_info.html",
        context={'user_cart': get_user_cart(request)}
    )

    cart_size_html = render_to_string(
        template_name="cart_size.html",
        context={'cart_size': get_cart_size(request)}
    )

    print("printing html")
    print(html)
    data_dict['html_from_view'] = html
    data_dict['html_cart_size'] = cart_size_html

    return JsonResponse(data=data_dict, safe=False)


@csrf_exempt
def checkout_details(request):
    if request.is_ajax():
        act = request.POST.get('act')
        if act == 'place_order':
            print("going to place_order")
            return place_order(request)
    else:
        return render(request, "checkout.html",
                      {'top_category_list': categoryview(), 'user_cart': get_user_cart(request),
                       'cart_size': get_cart_size(request)})


def write_review(request):
    print("in write review func")
    data_dict = {}
    if request.user.is_authenticated:
        given_id = int(request.POST.get('id'))
        rating = int(request.POST.get('rating'))
        review = request.POST.get('review')
        product = products.filter(id=given_id).first()
        if product is None:
            data_dict['error_msg'] = "product not found";
        else:
            ProductReview.objects.create(review=review, product_id=given_id, user_id=request.user.id, rating=rating)

    else:
        data_dict['error_msg'] = "Please login or register to leave a comment"
    return JsonResponse(data=data_dict, safe=False)


def reload_review(request):
    data_dict = {}
    given_id = int(request.POST.get('id'))
    print("in reload review product id : ")
    print(given_id)
    this_product_review = product_reviews.filter(product_id=given_id)
    print("this_product")
    print(this_product_review)
    html = render_to_string(
        template_name="single_review.html",
        context={'review': this_product_review}
    )
    html2 = render_to_string(
        template_name="review_length.html",
        context={'review': this_product_review}
    )
    print("printing html" + html)
    data_dict['html_from_view'] = html
    data_dict['html2_from_view'] = html2
    return JsonResponse(data=data_dict, safe=False)


@csrf_exempt
def product_details(request, product_id):
    print("asche")
    if request.is_ajax():
        act = request.POST.get('act')
        print("act" + act)
        if act == 'add_to_cart':
            return add_to_cart(request)
        elif act == 'write_review':
            return write_review(request)
        elif act == 'reload_review':
            return reload_review(request)
        elif act == 'add_to_wishlist':
            return add_to_wishlist(request)

    else:
        product = products.filter(id=product_id).first()
        print(product)
        print("getting product")
        this_product_review = product_reviews.filter(product_id=product_id)
        return render(request, 'product_details.html', {'product_details': product,
                                                        'products_list': products,
                                                        'shops_list': shops,
                                                        'review': this_product_review,
                                                        'cart_size': get_cart_size(request),
                                                        'top_category_list': categoryview(),
                                                        'user_cart': get_user_cart(request)})


def validate_user(request, username, email):
    try:
        user = User.objects.get(Q(username=username))
    except User.DoesNotExist:
        try:
            user = User.objects.get(Q(email=email))
        except User.DoesNotExist:
            user = None

    if user is not None:
        # user already exists
        return True
    else:
        return False


def login_user(request):
    if request.user.is_authenticated:
        print('dhukse')

        messages.add_message(request, messages.SUCCESS, 'You have already been logged in!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Welcome back!')
            return redirect('homepage')
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
    if request.user.is_authenticated:
        print('dhukse')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        profession = request.POST.get('profession')
        mobile_number = request.POST.get('mobile_no')
        bkash_account_no = request.POST.get('bkash_no')
        username = request.POST.get('user_name')
        password = request.POST.get('password')

        if validate_user(request, username, email):
            # user already exists
            msg = "User with this username or email already exists! :("
            messages.add_message(request, messages.ERROR, msg)

            return render(request, 'userreg.html', {
                'user_state': "exists",
            })
        else:

            # new user
            user = User.objects.create_user(username, email, password)

            user.profile.first_name = first_name
            user.profile.last_name = last_name
            user.profile.address = address
            user.profile.profession = profession
            user.profile.mobile_number = mobile_number
            user.profile.bkash_account_no = bkash_account_no

            user.save()

            login(request, user)
            msg = "Welcome to E-shop !"
            messages.add_message(request, messages.SUCCESS, msg)
            """
            @send user greetings
            """
            return homepage_view(request)

    else:
        return render(request, 'userreg.html')


def add_product(request):
    if not request.user.is_authenticated:
        print('dhukse')
        msg = "Please Login or Register"
        messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        qty = request.POST.get('quantity')
        price = request.POST.get('price')
        image = request.POST.get('image')
        catid = int(request.POST.get('category'))
        print(catid)
        category = CategoryTag.objects.get(Q(id=catid))
        print(catid)
        print("printing image attr")
        print(image)
        image = "img/" + category.category.lower() + "/" + image
        print(image)

        Product.objects.create(name=product_name, description=description, quantity=qty,
                               price=price, category=category, image=image, owner=request.user)

        msg = "Product has been added"
        messages.add_message(request, messages.SUCCESS, msg)
        """
        @send user greetings
        """
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return render(request, 'addproduct.html', {'category_list': cattag})


@login_required
def logout_user(request):
    logout(request)
    msg = "Hope to see you soon! :)"
    messages.add_message(request, messages.INFO, msg)
    return redirect('login_user')
