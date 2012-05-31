import os
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils.datastructures import MultiValueDictKeyError
from FlashCards import settings
from FlashCards.accounts.forms import *
from FlashCards.accounts.models import UserProfile
from FlashCards.apps.views import random_string

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
@login_required
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
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
            )
            user.first_name = form.cleaned_data['name']
            user.save()
            try:
                UserProfile.objects.create(
                    user = user,
                    #avatar =
                )
            except SuspiciousOperation:
                pass
            try:
                send_mail('[Flashcards G8] Registration',
                    render_to_response('regis_email.txt', {
                        'name': user.first_name,
                        'username': user.username,
                        'host': request.META['HTTP_HOST']
                    }),
                    'info@example.com',
                    [user.email]
                )
            except :
                pass
            login(request, authenticate(username=user.username, password=form.cleaned_data['password1']))
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'head_title': 'Sign Up',
        'title': 'ENGRADE SIGNUP',
        'form': form,
        'show_topnav': False
    } )
    return render_to_response('accounts/register.html',variables  )

@login_required
def usercp(request):
    try:
        action = request.GET['action']
    except MultiValueDictKeyError:
        return HttpResponseRedirect('?action=account')
    avatar = UserProfile.objects.get(user=request.user).getAvatarUrl()
    var = RequestContext(request, {
        'head_title': 'Account',
        'name': request.user.first_name,
        'avatar':avatar,
        'action':action,
        'path': request.META['PATH_INFO']
    })
    return render_to_response('accounts/usercp.html', var)

@login_required
def upload_file(request):
    url = UserProfile.objects.get(user=request.user).getAvatarUrl()
    if request.method == 'POST':
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            if url != settings.DEFAULT_AVATAR and os.path.exists(url):
                os.remove(url)
            u = UserProfile.objects.get(user=request.user)
            u.avatar = request.FILES['docfile']
            u.save()
            return HttpResponseRedirect('')
    else:
        form = UploadForm()
    documents = RequestContext(request, {
        'avatar':url,
        'form' : form
    })
    return render_to_response('accounts/upload.html', documents)

@login_required
def edit_account(request):
    if request.method == 'POST':
        form1 = ChangeNameForm(request.POST)
        form2 = ChangePasswordForm(request.POST)
        if form1.is_valid() & form2.is_valid():
            user = User.objects.get(username__exact=request.user.username)
            user.first_name = request.POST['name']
            user.email = request.POST['email']
            if request.POST['newPassword'] != '':
                user.set_password(request.POST['newPassword'])
            user.save()
            return HttpResponseRedirect('')
    else:
        list = dict([])

        try:
            list['name']= request.user.first_name
            list['email'] = request.user.email
        except:
            pass

        form1 = ChangeNameForm(list)
        form2 = ChangePasswordForm()

    var = RequestContext(request, {
        'form1': form1,
        'form2': form2,
        })
    return render_to_response('accounts/edit_account.html', var)

def lost_pass(request):
    if request.method == "POST":
        form = LostPassForm(request.POST)
        if form.is_valid():
            content = request.POST['name_or_mail']
            if '@' in content:
                user = User.objects.get(email=content)
            else:
                user = User.objects.get(username=content)

            rand_pass = random_string(8)

            send_mail('[Flashcards G8] Reset Engrade Password',
                render_to_response('reset_pass_mail.txt', {
                    'name': user.first_name,
                    'username': user.username,
                    'password': rand_pass,
                    'host': request.META['HTTP_HOST']
                }),
                'info@example.com',
                [user.email]
            )

            user.set_password(rand_pass)
            user.save()
            return HttpResponseRedirect('/')
    else:
        form = LostPassForm()

    var = RequestContext(request, {
        'title': 'FORGOT PASSWORD',
        'form': form,
    })
    return render_to_response('accounts/reset_password.html', var)