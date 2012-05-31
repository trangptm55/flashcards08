"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client

class UserTest(TestCase):
    def testChangePassword(self):
        user = User.objects.create(username = 'nobita', email = 'nobita@gmail.com', password = 'nobita')
        user.set_password('123456')
        c = Client()
        response = c.post('/accounts/login/', {'username': 'nobita', 'password': '123456'})
        self.assertEqual(response.status_code, 200)

class LoginPageTest(TestCase):
    def testLogin(self):
        c = Client()
        response = c.post('/accounts/login/', data={'username': 'mail', 'password': '123456'})
        self.assertEqual(response.status_code, 200)

    def testLoginFailPassword(self):
        c = Client()
        response = c.post('/accounts/login', data={'username': 'mailmail', 'password': 'mailmail'})
        self.assertEqual(response.status_code, 301)

class RegisterTest(TestCase):
    def testRegister(self):
        c = Client()
        response = c.post('/accounts/register/', data={'username': 'mailmail', 'email': 'mm@gmail.com', 'password1': '123456', 'password2': '123456'})
        self.assertEqual(response.status_code, 200)
