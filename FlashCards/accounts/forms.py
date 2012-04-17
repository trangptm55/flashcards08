from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class RegistrationForm(forms.Form):
    name = forms.CharField(
        label='Your Name',
        help_text='Enter your name as you wish others to see',
        widget=forms.TextInput(attrs = {'size':28})
    )
    email = forms.EmailField(
        label='Your Email',
        initial='email@example.com',
        help_text='Enter your valid email',
        widget=forms.TextInput(attrs = {'size':28})
    )
    username = forms.CharField(
        label='Choose Username',
        help_text='Choose username, letters, numbers and underscore only',
        max_length=20,
        min_length=3,
        widget=forms.TextInput(attrs = {'size':28})
    )
    password1 = forms.CharField(
        label='Choose Password',
        help_text='Choose your password',
        widget=forms.PasswordInput(attrs = {'size':28}),
        min_length=6,
    )
    password2 = forms.CharField(
        label='Confirm Password',
        help_text='Re-enter your password',
        widget=forms.PasswordInput(attrs = {'size':28}),
        min_length=6,
    )

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    def clean_email(self):
        bad_domains = ['mailinator.com']

        if User.objects.filter(email__iexact=self.cleaned_data['email']).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in bad_domains:
            raise forms.ValidationError("Registration using free email addresses is prohibited. Please supply a different email address.")
        return self.cleaned_data['email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=20,
        widget=forms.TextInput(attrs = {'size':28})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs = {'size':28}),
    )
    remember = forms.BooleanField(
        label='Keep me logged in on this computer',
        #label='',
        required=False
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username__exact=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError('Invalid username')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            user = User.objects.get(username=self.clean_username())
        except :
            raise forms.ValidationError('Invalid password')
        if user.check_password(password):
            return password
        raise forms.ValidationError('Invalid password')
