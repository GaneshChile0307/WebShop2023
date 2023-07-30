from .models import Category

def category_menu_links(request):
    menu_links = Category.objects.all()
    return dict(links=menu_links)