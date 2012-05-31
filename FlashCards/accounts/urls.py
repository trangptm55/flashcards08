from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template
from FlashCards.accounts.views import *

urlpatterns = patterns('',
    (r'^login/$', login_page),
    (r'^logout/$', logout_page),
    (r'^register/$', register_page),
    (r'^lost/$', lost_pass),
)
