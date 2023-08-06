
from django.http import HttpResponse 
from django.shortcuts import render , redirect
from cart.models import CartItem ,Cart
from store.models import Products

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
        print(cart)
    return cart


def add_cart(request, product_id):
    products = Products.objects.get(id=product_id)
    try:
        cart  = Cart.objects.get(cart_id=_cart_id(request))
        print(cart)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        print(cart)
    cart.save()


    try:
        cart_item = CartItem.objects.get(product=products,cart=cart)
        cart_item.quantity+=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = products,
            cart =cart , 
            quantity = 1
        )
        cart_item.save()
    return redirect('cart')

    


def cart(request, total=0 , quantity=0 ,cart_items=None):

    try:
        cart = Cart.objects.get(card_id= _cart_id(request))
        cart_items  = CartItem.objects.filter(cart=cart ,is_active=True)
        print("cart_items")
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except Exception as e:
        pass
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items
    }

    return render(request , 'store/cart.html', context)