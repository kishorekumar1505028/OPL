from django import template

register = template.Library()

foo = 0


@register.filter(name='get_min_max')
def get_min_max(item_list):
    min_val = 999999999
    max_val = 0
    for i in item_list:
        pval = float(i.price)
        if pval < min_val:
            min_val = pval
        if pval > max_val:
            max_val = pval
    return {int(min_val), int(max_val)}


@register.filter(name='get_brand')
def get_brand(name):
    return name[0:name.find(' ')]


@register.filter(name='cart_total_price')
def cart_total_price(carts):
    total = 0
    for cart in carts:
        total += cart.quantity * cart.product.price
    return total


@register.filter(name='get_part_totoal')
def get_part_totoal(price, arg):
    total = price * arg
    return total


@register.filter(name='getrange')
def getrange(value, arg):
    if arg == 0:
        return range(value)
    else:
        return range(arg - value)


@register.filter(name='getval')
def getval(value):
    return int(value)


@register.filter(name='getfoo')
def getfoo(val):
    return val


@register.filter(name='setfoo')
def setfoo(val):
    foo = 2
    print("foo : ")
    print(foo)


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter(name='getcategory')
def getcategory(item_list, arg):
    category_list = [arg]

    if item_list is None:
        return category_list

    for i in item_list:
        set_category_list = set(category_list)
        if arg == "All Categories":
            if i.category in set_category_list:
                pass
            else:
                category_list.append(i.category)
        elif arg == "Any Location":
            if i.location in set_category_list:
                pass
            else:
                category_list.append(i.location)

    return category_list
