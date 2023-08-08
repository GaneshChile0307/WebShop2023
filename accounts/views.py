from django.shortcuts import render ,redirect
from django.contrib import auth 
from accounts.form import RegistartionFrom
from accounts.models import Account
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from cart.models import Cart, CartItem
from cart.views import _cart_id



# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage 
# Create your views here.

def register(request):

    if request.method == 'POST':
        form = RegistartionFrom(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user= Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.phone_number = phone_number
            user.save()

            #user activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message =  render_to_string('account/account_verify_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject , message , to=[to_email])
            send_email.send()

            return redirect('/account/login/?command=verification&email='+email)


    else:
        form = RegistartionFrom()
    
    context = {
        "form" : form
    }
    return render(request,'account/register.html',context)



def activate(request,uidb64 ,token):
    try:
        uid =  urlsafe_base64_decode(uidb64)
        user= Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        print(e)
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists =  CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                for item in cart_item:
                    item.user = user
                    item.save()
            except :
                pass
            auth.login(request,user)        
            return redirect('home')
        else:
             return redirect('login')

    return render(request,'account/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    # orders = Order.object.order_by('-created_by').filter(user_id=request.user.id,is_ordered=True)
    return render(request, 'account/dashboard.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            #sending forgot pass link
            current_site = get_current_site(request)
            mail_subject = 'Please reset your account password'
            message =  render_to_string('account/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject , message , to=[to_email])
            send_email.send()
            return redirect('login')

        else:
            return redirect('register')

    return render(request, 'account/forgotPassword.html')


def resetpassword_validate(request,uidb64 ,token):
    try:
        uid =  urlsafe_base64_decode(uidb64).decode()
        user= Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        print(e)
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('resetPassword')
    else:
        return HttpResponse('The link has expired')
    

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            return redirect('login')
        else:
            return redirect('resetPassword')
    else:
        return render(request , 'account/resetPassword.html')
       
    