from django.conf.urls.defaults import *
from settings import PROJECT_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^ratings/', include('ratings.ratings4you.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    #captcha
    url(r'^captcha/', include('captcha.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('ratings.registration.urls')),
    
    
    #css
    (r'^css/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '%s/media/css' % (PROJECT_ROOT)}),
    #js
    (r'^js/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '%s/media/js' % (PROJECT_ROOT)}),
    #images
    (r'^images/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '%s/media/i' % (PROJECT_ROOT)}),
)
