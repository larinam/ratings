'''
Created on 19.06.2010

@author: alarin
'''
from django.conf.urls.defaults import *

urlpatterns = patterns('',
   (r'^$', 'ratings.ratings4you.views.index'),
   (r'^accounts/profile/$', 'ratings.ratings4you.accounts.profile'),
                       
)