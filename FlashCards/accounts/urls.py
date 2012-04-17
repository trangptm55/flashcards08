from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template
from accounts.views import *

urlpatterns = patterns('',
    (r'^login/$', login_page),
    (r'^logout/$', logout_page),
    (r'^register/$', register_page),
    (r'^register/success/$', direct_to_template,
         { 'template': 'accounts/register_success.html'}),
)
