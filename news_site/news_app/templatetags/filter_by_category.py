from django import template

register = template.Library()

@register.filter(name="filter_by_category")
def filter_by_category(object_list, category_name):
    counter = 0
    category_list = []
    for object in object_list:
        if object.category == category_name:
            if counter <= 5:
                category_list.append(object)
                counter += 1
            else:
                break
    return category_list

@register.filter(name="filter_by_category_2")
def filter_by_category_2(object_list, category_name):
    category_list = []
    for object in object_list:
        if object.category == category_name:
            category_list.append(object)
    return category_list

@register.filter(name="filer_by_search")
def filter_by_search(category_list, search_term):
    search_list = [] 
    for object in category_list:
        if search_term.lower() in object.title.lower():
            search_list.append(object)
    return search_list