from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from FlashCards.accounts.forms import *
from FlashCards.accounts.models import UserProfile

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if not request.POST.get('remember', None):
                request.session.set_expiry(0)
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse('Your account is not active')
            else:
                HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    var = RequestContext(request, {
        'head_title': 'Login',
        'title':'ENGRADE LOGIN',
        'form':form,
        'show_topnav':True
    })
    return render_to_response('accounts/login.html', RequestContext(request, var))

def logout_page(request):
    if request.method == 'POST':
        return login_page(request=request)
    else:
        logout(request)
    var = RequestContext(request, {
        'head_title': 'Logout',
        'title': 'YOU\'VE BEEN LOGGED OUT',
        'form': LoginForm(),
        'show_topnav':True
    })
    return render_to_response('accounts/login.html', RequestContext(request, var))

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                first_name = form.cleaned_data['name']
            )
            UserProfile.objects.create(
                user = user,
            )
            #from django.core.mail import send_mail
            #recipients = ['info@example.com']
            #send_mail('Registration', 'Thanks for your registration', recipients, [form.cleaned_data['email']] )
            return HttpResponseRedirect('/accounts/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'head_title': 'Sign Up',
        'title': 'ENGRADE SIGNUP',
        'form': form,
        'show_topnav': False
    } )
    return render_to_response('accounts/register.html',variables  )

