'''
Created on 19.06.2010

@author: alarin
'''
from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
   (r'^$', 'ratings.ratings4you.views.index'),
   (r'^accounts/profile/$', 'ratings.ratings4you.accounts.profile'),
   (r'^add/$', 'ratings.ratings4you.views.add'),
   (r'^additem/(?P<id>\w{0,10})/$', 'ratings.ratings4you.views.add_item'),
   (r'^view/(?P<id>\w{0,10})/$', 'ratings.ratings4you.views.view_rating'),
   (r'^view_results/(?P<id>\w{0,10})/$', 'ratings.ratings4you.views.view_rating_results'),
   (r'^sendtomoder/(?P<id>\w{0,10})/$', 
    'ratings.ratings4you.views.send_to_moderator'),
   (r'^feedback/$', 'ratings.ratings4you.views.feedback'),
   
   #administration
   (r'^admin/$', 'ratings.ratings4you.views_admin.index'),
   (r'^admin/catalogs/$', 'ratings.ratings4you.views_admin.catalogs'),
   
   (r'^admin/catalogs/themes/$', 'ratings.ratings4you.views_admin.themes'),
   (r'^admin/catalogs/regions/$', 'ratings.ratings4you.views_admin.regions'),
   (r'^admin/catalogs/themes/(?P<id>\w{0,10})/$', 'ratings.ratings4you.views_admin.themes'),
   (r'^admin/catalogs/regions/(?P<id>\w{0,10})/$', 'ratings.ratings4you.views_admin.regions'),
   
   (r'^admin/moderation/$', 'ratings.ratings4you.views_admin.moderation'),
   (r'^admin/moderaterating/(?P<id>\w{0,10})/$', 
    'ratings.ratings4you.views_admin.moderate_rating'),
   (r'^admin/rating_send_mail$', 'ratings.ratings4you.views_admin.rating_send_mail'),
   (r'^admin/moderator_email/$', 'ratings.ratings4you.views_admin.moderator_email'),
   (r'^admin/edit_unmoderated_items/(?P<id>\w{0,10})/$', 'ratings.ratings4you.views_admin.edit_unmoderated_items'),
   (r'^admin/catalogs/themes/edit/(?P<id>\w{0,10})/$',
    'ratings.ratings4you.views_admin.edit_theme_item'),                        
   (r'^admin/catalogs/regions/edit/(?P<id>\w{0,10})/$',
    'ratings.ratings4you.views_admin.edit_region_item'),
)