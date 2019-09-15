from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

from products.models import Cart, WishList
from .models import Product
from .models import Shop, TopCategory, TopSuper, CategoryTag, SuperCategory, ProductReview, PurchaseLog
from products.forms import ProductForm

PENDING = 0
DONE = 1
STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (DONE, 'Done'),
]

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

        super_category_list = []

        for j in tempsuper:

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

            filtered_products = filtered_products.filter(price__range=(minval, maxval)).order_by(sortby)
            if reverselist == 'true':
                filtered_products = filtered_products.reverse()

            html = render_to_string(
                template_name="category_page_product_info.html",
                context={'products_list': filtered_products}
            )

            data_dict = {"html_from_view": html}

            return JsonResponse(data=data_dict, safe=False)


@csrf_exempt
def add_to_or_remove_from_cart(request, is_checkout=0, add_or_change=1):
    data_dict = {}
    if request.user.is_authenticated:

        given_id = int(request.POST.get('product_id'))
        given_qty = int(request.POST.get('numbers'))
        add_or_remove = int(request.POST.get('add_or_delete'))
        product_in_storage = products.filter(id=given_id)
        requested_product = Cart.objects.all().filter(user__id=request.user.id,
                                                      product_id=given_id)
        print(given_id)
        # remove
        if add_or_remove == 0:
            if requested_product:
                print("product found")
                requested_product.delete()
                data_dict['success_msg'] = "Product deleted"
            else:
                data_dict['error_msg'] = "Product shit not found" + str(given_id)

        # add
        else:
            if requested_product:

                if add_or_change:
                    new_quantity = requested_product.first().quantity + given_qty
                else:
                    new_quantity = given_qty
                if product_in_storage.first() is None:
                    data_dict['error_msg'] = "Product not found in Product storage"

                elif new_quantity > product_in_storage.first().quantity:
                    data_dict['error_msg'] = "The quantity of Product not available"

                else:
                    requested_product.update(quantity=new_quantity)
                    data_dict['success_msg'] = "Product quantity increased by " + str(new_quantity)
                    print(requested_product)
            else:
                if given_qty <= product_in_storage.first().quantity:
                    print("creating..")
                    Cart.objects.create(user_id=request.user.id, product_id=given_id, quantity=given_qty)
                    data_dict['success_msg'] = "Product added to cart"
                else:
                    data_dict['error_msg'] = "The quantity of Product not available"

    else:
        data_dict['error_msg'] = "Please login or register first"

    print("getting user cart")
    user_cart = get_user_cart(request)
    cart_size = get_cart_size(request)
    for rows in user_cart:
        print(rows.product.name)

    html = render_to_string(
        template_name="small_cart.html",
        context={'user_cart': user_cart}
    )

    if is_checkout:
        checkout_html = render_to_string(
            template_name="checkout_info.html",
            context={'user_cart': user_cart}
        )
        data_dict['checkout_info_html'] = checkout_html
    else:
        cart_html = render_to_string(
            template_name="cart_info.html",
            context={'user_cart': user_cart}
        )
        data_dict['cart_info_html'] = cart_html

    print("printing html")
    print(html)
    print("printing cart size html")

    data_dict['html_from_view'] = html

    data_dict['html_cart_size'] = cart_size

    return data_dict


@csrf_exempt
def add_to_wishlist(request):
    data_dict = {}
    if request.user.is_authenticated:

        given_id = int(request.POST.get('product_id'))
        add_or_delete = int(request.POST.get('add_or_delete'))
        product_in_storage = products.filter(id=given_id)
        requested_product = WishList.objects.all().filter(user__id=request.user.id,
                                                          product_id=given_id)
        print('add wishlist or remove')
        print(add_or_delete)
        if product_in_storage.first() is None:
            data_dict['error_msg'] = "Product not found"
        # remove
        elif add_or_delete == 0:

            if requested_product:
                print("product found")
                requested_product.delete()
                data_dict['success_msg'] = "Product deleted"
            else:
                data_dict['error_msg'] = "Product not found"

        # add
        else:
            if requested_product:
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

    return data_dict


@csrf_exempt
def homepage_view(request, id=0):
    if request.is_ajax():
        act = request.POST.get('act')
        if act == 'add_to_cart':
            data_dict = add_to_or_remove_from_cart(request)
            return JsonResponse(data=data_dict, safe=False)

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
        return render(request, 'homepage.html', context=ctx)


@login_required
@csrf_exempt
def advanced_search(request, category):
    if request.is_ajax():
        act = request.POST.get('act')
        if act == 'add_to_cart':
            data_dict = add_to_or_remove_from_cart(request)
            return JsonResponse(data=data_dict, safe=False)

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


@login_required
@csrf_exempt
def place_order(request):
    data_dict = {}

    if request.user.is_authenticated:
        user_cart = get_user_cart(request)

        if user_cart is None:
            data_dict['error_msg'] = 'Empty Cart'

        else:

            # check availability of each product
            for cart_item in user_cart:
                product_in_storage = Product.objects.all().filter(id=cart_item.product.id)
                if cart_item.quantity > product_in_storage.first().quantity:
                    data_dict[
                        'error_msg'] = 'The quantity of product' + product_in_storage.first().name + ' is not available'
                    return JsonResponse(data=data_dict, safe=False)

            # now insert in PurchaseLog
            for cart_item in user_cart:
                product_in_order_history = PurchaseLog.objects.all().filter(product_id=cart_item.product.id,
                                                                            user_id=request.user.id)
                if product_in_order_history:
                    c = 0
                    for product_in_order in product_in_order_history:

                        if product_in_order.orderStatus == PENDING:
                            # already has an entry
                            new_quantity = product_in_order.quantity + cart_item.quantity
                            product_in_order.quantity = new_quantity
                            product_in_order.save()
                            break
                        c += 1
                    print('c is ')
                    print(c)
                    print('product count ')
                    print(product_in_order_history.count())
                    if c == product_in_order_history.count():
                        # no previous pending entry

                        PurchaseLog.objects.create(quantity=cart_item.quantity, product_id=cart_item.product_id,
                                                   user_id=request.user.id, orderStatus=PENDING)
                        data_dict['success_msg'] = "Order pending for approval"
                else:
                    PurchaseLog.objects.create(quantity=cart_item.quantity, product_id=cart_item.product_id,
                                               user_id=request.user.id, orderStatus=PENDING)
                    data_dict['success_msg'] = "Order pending for approval"

            user_cart.delete()
    else:
        data_dict['error_msg'] = 'Please Register or Login first'

    cart_info_html = render_to_string(
        template_name="checkout_info.html",
        context={'user_cart': get_user_cart(request)}
    )

    data_dict['html_cart_size'] = get_cart_size(request)

    print("printing html")
    print(cart_info_html)
    data_dict['html_from_view'] = cart_info_html

    return JsonResponse(data=data_dict, safe=False)


@login_required
@csrf_exempt
def cart_details(request):
    if request.is_ajax():
        act = request.POST.get('act')
        if act == 'add_to_cart':
            data_dict = add_to_or_remove_from_cart(request, 0, 0)
            cart_total_html = render_to_string(
                template_name="cart_total.html",
                context={'user_cart': get_user_cart(request)}
            )
            data_dict['cart_total_html'] = cart_total_html
            return JsonResponse(data=data_dict, safe=False)
    else:

        return render(request, "cart.html", {'top_category_list': categoryview(), 'user_cart': get_user_cart(request),

                                             'cart_size': get_cart_size(request)})


@csrf_exempt
def get_vendor_storage(request):
    if request.user.is_authenticated:
        print("in get_user_cart function user is authenticated")
        print(request.user.id)
        vendor_storage = Product.objects.all().filter(owner__id=request.user.id)
        return vendor_storage
    else:
        return []


@csrf_exempt
def add_product_quantity(request):
    return 0


@csrf_exempt
def change_in_storage(request):
    data_dict = {}
    if request.user.is_authenticated:

        given_id = int(request.POST.get('id'))
        given_qty = int(request.POST.get('quantity'))
        given_price = float(request.POST.get('price'))
        change_or_remove = int(request.POST.get('change_or_remove'))
        requested_product = products.filter(id=given_id)
        print(given_id)
        # remove
        if change_or_remove == 0:
            if requested_product:
                print("product found")
                requested_product.delete()
                data_dict['success_msg'] = "Product deleted"
            else:
                data_dict['error_msg'] = "Product shit not found" + str(given_id)

        # change_quantity
        else:
            if requested_product:
                new_quantity = given_qty
                old_price = requested_product.first().price
                requested_product.update(quantity=new_quantity)

                if old_price != given_price:
                    requested_product.update(old_price=old_price)
                    requested_product.update(price=given_price)
                    discount = float(("{0:.2f}".format((old_price - given_price) / old_price * 100)))
                    print("discount")
                    print(discount)
                    requested_product.update(discount=discount)

                data_dict['success_msg'] = "Product quantity increased by " + str(new_quantity)
                print(requested_product)
    else:
        data_dict['error_msg'] = "Please login or register first"

    print("getting storage")

    vendor_storage = get_vendor_storage(request)
    for product in vendor_storage:
        print(product.name)

    storage_html = render_to_string(
        template_name="vendor_storage_info.html",
        context={'vendor_storage': vendor_storage}
    )
    data_dict['vendor_storage'] = storage_html

    print("printing html")
    print(storage_html)
    print("printing cart size html")

    return data_dict


@login_required
@csrf_exempt
def storage_details(request):
    if request.is_ajax():
        act = request.POST.get('act')
        if act == 'change':
            data_dict = change_in_storage(request)
            return JsonResponse(data=data_dict, safe=False)
    else:

        return render(request, "vendor_product_list.html", {'vendor_storage': get_vendor_storage(request)})


def get_order_request(request):
    pending_orders = PurchaseLog.objects.all().filter(user_id=request.user.id, orderStatus=PENDING)
    return pending_orders


def get_purchase_history(request):
    pending_orders = PurchaseLog.objects.all().filter(user_id=request.user.id, orderStatus=DONE)
    return pending_orders


def get_vendor_order_request(request):
    pending_orders = PurchaseLog.objects.all().filter(product__owner_id=request.user.id, orderStatus=PENDING)
    return pending_orders


def get_vendor_sale_history(request):
    pending_orders = PurchaseLog.objects.all().filter(product__owner_id=request.user.id, orderStatus=DONE)
    return pending_orders


@login_required
def order_request_details(request):
    return render(request, "order_request.html",
                  {'top_category_list': categoryview(), 'user_cart': get_user_cart(request),
                   'orders': get_order_request(request),
                   'cart_size': get_cart_size(request),
                   'title': 'Order Request Details'})


@login_required
def purchase_history_details(request):
    return render(request, "order_request.html",
                  {'top_category_list': categoryview(), 'user_cart': get_user_cart(request),
                   'orders': get_purchase_history(request),
                   'cart_size': get_cart_size(request),
                   'title': 'Purchase History Details'})


@login_required
def vendor_order_request_details(request):
    return render(request, "vendor_order_request.html", {'orders': get_vendor_order_request(request),
                                                         'title': 'Pending Requests Details'})


@login_required
def vendor_sale_history_details(request):
    return render(request, "vendor_order_request.html", {'orders': get_vendor_sale_history(request),
                                                         'title': 'Sale History Details'})


@login_required
@csrf_exempt
def wishlist_details(request):
    if request.is_ajax():

        act = request.POST.get('act')

        if act == 'add_to_cart':
            data_dict = add_to_or_remove_from_cart(request, 0, 1)

        elif act == 'add_to_wishlist':
            print('calling add_to_wishlist')
            data_dict = add_to_wishlist(request)

        user_wishlist_html = render_to_string(
            template_name="wishlist_info.html",
            context={'user_wishlist': get_user_wishlist(request)}
        )

        data_dict['wishlist_info_html'] = user_wishlist_html

        return JsonResponse(data=data_dict, safe=False)

    return render(request, "wishlist.html",
                  {'top_category_list': categoryview(), 'user_wishlist': get_user_wishlist(request),
                   'cart_size': get_cart_size(request), 'user_cart': get_user_cart(request)})


@login_required
@csrf_exempt
def checkout_details(request):
    if request.is_ajax():

        act = request.POST.get('act')

        if act == 'place_order':
            print("going to place_order")
            return place_order(request)

        elif act == 'add_to_cart':

            data_dict = add_to_or_remove_from_cart(request, 1)
            checkout_total_html = render_to_string(
                template_name="checkout_total.html",
                context={'user_cart': get_user_cart(request)}
            )

            data_dict['checkout_total_html'] = checkout_total_html

            return JsonResponse(data=data_dict, safe=False)
    else:
        return render(request, "checkout.html",
                      {'top_category_list': categoryview(), 'user_cart': get_user_cart(request),
                       'cart_size': get_cart_size(request)})


@login_required
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


@login_required
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
@login_required
def product_details(request, product_id):
    print("asche")
    if request.is_ajax():
        act = request.POST.get('act')
        print("act" + act)
        if act == 'add_to_cart':
            data_dict = add_to_or_remove_from_cart(request)
            return JsonResponse(data=data_dict, safe=False)

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


def vendor_homepage_view(request):
    if request.user.is_authenticated:
        return render(request, 'vendor_homepage.html', {})


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
            messages.add_message(request, messages.SUCCESS, 'Welcome back ' + request.user.username + '!')
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
            return homepage_view(request, 1)

    else:
        return render(request, 'userreg.html')


def add_product(request):
    if not request.user.is_authenticated:
        print('dhukse')
        msg = "Please Login or Register"
        messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)

        if product_form.is_valid():
            new_product = product_form.save(commit=False)
            new_product.owner = request.user
            new_product.save()
            msg = "Product has been added"
            messages.add_message(request, messages.SUCCESS, msg)

        else:
            msg = "Adding Product Failed"
            messages.add_message(request, messages.ERROR, msg)

        """
        @send user greetings
        """

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        form = ProductForm()
        return render(request, 'addproduct.html', {'category_list': cattag, 'form': form})


@login_required
def logout_user(request):
    logout(request)
    msg = "Hope to see you soon! :)"
    messages.add_message(request, messages.INFO, msg)
    return redirect('login_user')
