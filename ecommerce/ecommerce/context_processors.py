from products.models import Category

def navigation(request):
    category_list = []
    all_categories = list(Category.objects.all())
    for category in all_categories:
        if category.children.all():
            category_list.append({category: list(category.children.all())})
        elif category.parent:
            pass
        else:
            category_list.append({category: None})
    return {'category_list': category_list}
    