from captcha.fields import *
from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import filesizeformat
from FlashCards import settings
from django.utils.translation import ugettext_lazy as _

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

class UploadForm(forms.Form):
    docfile = forms.FileField(
        label = 'Select a file',
    )

    def clean_docfile(self):
        content = self.cleaned_data['docfile']
        content_type = content.content_type.split('/')[0]
        if content_type in settings.CONTENT_TYPES:
            if content._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
        else:
            raise forms.ValidationError(_('File type is not supported'))
        return content

class ChangePasswordForm(forms.Form):

    newPassword = forms.CharField(
        label='New Password',
        help_text='Enter a new password',
        widget=forms.PasswordInput(attrs = {'size':28}),
        min_length=6,
        required=False
    )

    confirmPassword = forms.CharField(
        label='Confirm New Password',
        help_text='Enter above password',
        widget=forms.PasswordInput(attrs = {'size':28}),
        min_length=6,
        required=False
    )

    def clean_confirmPassword(self):
        if 'newPassword' in self.cleaned_data:
            newPassword = self.cleaned_data['newPassword']
            confirmPassword = self.cleaned_data['confirmPassword']
            if newPassword == confirmPassword:
                return confirmPassword
            raise forms.ValidationError('Passwords do not match.')



class ChangeNameForm(forms.Form):
    name = forms.CharField(
        label = 'Your Name',
        help_text = 'Enter your full name',
        widget=forms.TextInput(attrs = {'size':28}),
    )

    email = forms.EmailField(
        label = 'Email',
        help_text = 'Enter your email address',
        widget=forms.TextInput(attrs = {'size':28}),
    )

class LostPassForm(forms.Form):
    namOrEmail = forms.CharField(
        label='Username or Email',
        help_text='Enter your username or email address',
        widget=forms.TextInput(attrs={'size':28})
    )
    captcha = CaptchaField(
        help_text='Enter the numbers in the box',
        label='Code',
        #widget=CaptchaTextInput(attrs={'size':28})
    )

    def cleanOrEmail(self):
        content = self.cleaned_data['name_or_mail']
        if '@' in content:
            try:
                User.objects.get(email=content)
            except ObjectDoesNotExist:
                raise forms.ValidationError('Invalid username/email')
            return content
        else:
            try:
                User.objects.get(username=content)
            except ObjectDoesNotExist:
                raise forms.ValidationError('Invalid username/email')
            return content