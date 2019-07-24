from django import template

register = template.Library()

foo = 0

@register.filter(name='getrange')
def getrange(value, arg):
    if arg == 0:
        return range(value)
    else:
        return range(arg - value)

@register.filter(name='getval')
def getval (value):
    return value\

@register.filter(name='getfoo')
def getfoo (val):
    return foo
@register.filter(name='setfoo')
def setfoo (val):
    foo = 2
    print("foo : ")
    print(foo)

@register.filter(name='getcategory')
def getcategory(item_list , arg):
    category_list = [arg]

    if item_list is None:
        return category_list

    for i in item_list:
        set_category_list = set(category_list)
        if arg == "All Categories" :
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
