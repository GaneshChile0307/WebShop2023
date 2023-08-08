from django.shortcuts import render,get_object_or_404
from store.models import Products
from category.models import Category

# Create your views here.
def store(request,category_slug=None):
    categories=None
    product = None

    if category_slug != None:
        categories =get_object_or_404(Category , slug=category_slug)
        product =Products.objects.filter(category = categories ,is_available=True)
        product_count = product.count()
    else:
        product = Products.objects.all().filter(is_available=True)
        product_count = product.count()
    context = {
        'products' : product,
        'product_count' : product_count,
    }
    return render(request, 'store/store.html',context)


def product_detail(request,category_slug,product_slug):
    print("inside product details")
    try:
        single_product = Products.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e
    print(single_product.price)
    context = {
        'single_product': single_product,
    }
    return render(request, 'store/product_detail.html',context)