import os
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from FlashCards.accounts.views import *
from FlashCards.apps.views import *
from FlashCards.main.views import *

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'FlashCards.views.home', name='home'),
    # url(r'^FlashCards/', include('FlashCards.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Browsing
    (r'^$', main_page),
    (r'^app/$', user_page),
    (r'^user/$', usercp),
    (r'^show/(\w+)', show_prompt),
    (r'^like/(\w+)', like),
    (r'^dir/(\w+)', dir_subj),
    (r'^dir/$', dir_page),

    # iFrame
    (r'^iframe/form/$', flashcard_page),
    (r'^iframe/picture/$', upload_file),
    (r'^iframe/account/$', edit_account),

    # Account management
    (r'^accounts/', include('accounts.urls')),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': os.path.join(os.path.dirname(__file__), 'site_media')}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': os.path.join(os.path.dirname(__file__), 'media')}),

    url(r'^captcha/', include('captcha.urls')),

    # Test
    (r'^test/$', test),

    (r'^init/$', init)
)