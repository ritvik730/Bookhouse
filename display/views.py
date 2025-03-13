from django.shortcuts import render, redirect, HttpResponsePermanentRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib import messages
from display.models import *
from django.db.models import Q
import uuid
from display.mails import *
from display.helpers import send_forget_password_mail
from django.views.decorators.cache import cache_control


def index_page(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        error_msg = ""
        if not name:
            error_msg = "Enter your name !"
        if not email:
            error_msg = "Enter your email !"
        if not phone:
            error_msg = "Enter your phone !"
        if not message:
            error_msg = "Enter your message !"
        if not error_msg:
            contact = Contact(name=name, email=email,
                              phone=phone, message=message)
            contact.save()
            context = {"name": name, "email": email,
                       "phone": phone, "message": message}
            mail_to_admin(context)
            messages.info(
                request, "Your message was sent, We'll contact you soon, Thank you!")
        else:
            context = {'error_condition': error_msg}
            return render(request, "contact.html", context)
    return render(request, "contact.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request, item=0):
    if request.user.is_anonymous:
        return redirect('/')
    if (request.method == 'GET' and item == 0): 
        categories = Category.objects.all()
        product = Product.objects.filter(status=1)
        
        
        # cart_total = Cart.objects.filter(user=request.user).count
        context = {'products': product, 'category':categories}
        return render(request, "dashboard.html", context)
    elif (request.method == 'GET' and item != 0): 
        
        categories = Category.objects.all()  # fetching all categories
        result = Product.objects.filter(Q(category=item) & Q(status=1))
        context = {'products': result, 'category':categories}
        return render(request, "dashboard.html", context)
    
    elif (request.method == 'POST' and item == 0): 
        search = request.POST.get('search')
        if search == '':
            return redirect('/dashboard/0')
        categories = Category.objects.all()
        product = Product.objects.filter((Q(product_title=search) | Q(
                prod_desc=search)) & Q(status=1) ) 
    
        context = {'products': product, 'category':categories,'value':search}
        return render(request, "dashboard.html", context)
    return render(request,"dashboard.html")

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        registerd = User.objects.filter(email=email).exists()
        error_msg = ""
        if(registerd):
            loggedinuser = User.objects.get(email=email)

            profile_obj = Profile.objects.filter(username=loggedinuser).first()

            if not profile_obj.is_verified:
                error_msg = "email hasn't verified,check your mail"
                context = {"error_condition": error_msg}
                return render(request, 'login.html', context)

            if(loggedinuser.check_password(password)):
                auth.login(request, loggedinuser)

                return redirect('/dashboard/0')
            else:
                error_msg = "Incorrect Password"
                context = {"error_condition": error_msg}
                return render(request, "login.html", context)
        else:
            error_msg = "email hasn't registered"
            context = {"error_condition": error_msg}
            return render(request, "login.html", context)
    return render(request, "login.html")


def logouts(request):
    logout(request)
    return HttpResponsePermanentRedirect("/")


def forget_pass(request):
    if request.method == 'POST':
        useremail = request.POST.get('email')
        if not useremail:
            messages.info(request, 'Please enter you email ID !')
            return redirect('/forget_pass/')
        if not User.objects.filter(email=useremail).exists():
            messages.info(request, 'No Account exists with this email !')
            return redirect('/forget_pass/')
        else:
            usr_obj = User.objects.get(email=useremail)
            token = str(uuid.uuid4())        # generating unique token
            resetprofile_obj = ResetProfile.objects.get(user=usr_obj)
            resetprofile_obj.forget_password_token = token
            resetprofile_obj.save()
            send_forget_password_mail(usr_obj.email, token)
            messages.success(
                request, "Password reset link has sent to your mail.")
            return redirect('/forget_pass/')
    return render(request, "forget_pass.html")


def change_pass(request, token):

    resetprofile_obj = ResetProfile.objects.filter(
        forget_password_token=token).first()
    if not resetprofile_obj:
        return redirect('/reseterror/')
    context = {'user_id': resetprofile_obj.user.id}
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user_id = request.POST.get('user_id')

        if user_id is None:
            messages.success(request, 'No user id found ! ')
            return redirect(f'/change_pass/{token}/')

        if new_password != confirm_password:
            messages.success(request, 'Both passwords does not match !')
            return redirect(f'/change_pass/{token}/')

        user_obj = User.objects.get(id=user_id)
        user_obj.set_password(new_password)
        user_obj.save()
        resetprofile_obj.forget_password_token = None
        resetprofile_obj.save()
        passChangedMsg = {'msg': 'Password changed successfully'}
        # return redirect('/login/',passChangeSuccess)
        return render(request, "login.html", passChangedMsg)

    # print(profile_obj)
    return render(request, "change_pass.html", context)


# def room(request):
#     if request.user.is_anonymous:
#         return redirect('/')
#     return render(request, "room.html")


def service(request):
    return render(request, "service.html")


def reseterror(request):
    return render(request, "reseterror.html")


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        error_msg = ""
        if(password != cpassword):
            error_msg = "Password didn't match"
            context = {"password_error": error_msg}
            return render(request, "signup.html", context)

        check = User.objects.filter(email=email).exists()
        if check:
            print('email registerd')
            error_msg = "email already registered"
            context = {"error_condition": error_msg}
            return render(request, "signup.html", context)
        elif User.objects.filter(username=username).exists():
            print('already username')
            error_msg = "username has already taken"
            context = {"username_error": error_msg}
            return render(request, "signup.html", context)
        else:
            signups = User.objects.create_user(username=username,  email=email,
                                               password=password)
            signups.save()
            profile_obj = ResetProfile.objects.create(user=signups)
            profile_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(
                username=signups, auth_token=auth_token)

            profile_obj.save()
            user_profile = UserProfile.objects.create(user=signups)
            user_profile.save()
            send_mail_after_registration(email, auth_token)
            context = {"mail_sent": 'Activation link has sent to your mail'}
            return render(request, "signup.html", context)

    return render(request, "signup.html")


def token(request):
    print('hellp')
    return render(request, 'token.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                print('verified already')
                context = {
                    "verify_message": 'Your account is already verified.'}
                return render(request, "token.html", context)
            print('success')
            profile_obj.is_verified = True
            profile_obj.save()
            context = {
                "verify_message": 'Your account verified successfully.'}
            # user_profile = UserProfile.objects.create(user=profile_obj)
            # user_profile.save()
            return render(request, "token.html", context)
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')


def error_page(request):
    return render(request, 'error.html')


def send_mail_after_registration(email, token):
    header = "Verify Your Account | BookHouse"
    link = f'http://127.0.0.1:8000/verify/{token}'
    button = 'VERIFY MY EMAIL'
    content = 'verify your email'
    heading = 'Verify Your Email'
    context = {"email": email, "header": header,
               "link": link, "button": button, "content": content, "heading": heading}
    mail_sent(context)

    # subject = "Your account need to be verify"
    # message = f'Hi paste the llink to verify your account  http://127.0.0.1:8000/verify/{token}'
    # email_from = settings.EMAIL_HOST_USER
    # recipient_list = [email]
    # send_mail(subject, message, email_from, recipient_list)
