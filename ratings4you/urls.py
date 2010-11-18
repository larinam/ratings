'''
Created on 19.06.2010

@author: alarin
'''
from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
   (r'^$', 'ratings4you.views.index'),
   (r'^accounts/profile/$', 'ratings4you.accounts.profile'),
   (r'^add/$', 'ratings4you.views.add'),
   (r'^additem/(?P<id>\w{0,10})/$', 'ratings4you.views.add_item'),
   (r'^view_list/(?P<id>\w{0,10})/$', 'ratings4you.views.view_ratings_list'),
   (r'^view/(?P<id>\w{0,10})/$', 'ratings4you.views.view_rating'),
   (r'^view_results/(?P<id>\w{0,10})/$', 'ratings4you.views.view_rating_results'),
   (r'^sendtomoder/(?P<id>\w{0,10})/$', 
    'ratings4you.views.send_to_moderator'),
   (r'^feedback/$', 'ratings4you.views.feedback'),
   (r'^about/$', 'ratings4you.views.development_message'),
   (r'^forum/$', 'ratings4you.views.development_message'),
   (r'^analitics/$', 'ratings4you.views.development_message'),
   (r'^arch/$', 'ratings4you.views.development_message'),
   (r'^exp/$', 'ratings4you.views.development_message'),
   
   #administration
   (r'^admin/$', 'ratings4you.views_admin.index'),
   (r'^admin/catalogs/$', 'ratings4you.views_admin.catalogs'),
   
   (r'^admin/catalogs/themes/$', 'ratings4you.views_admin.themes'),
   (r'^admin/catalogs/regions/$', 'ratings4you.views_admin.regions'),
   (r'^admin/catalogs/themes/(?P<id>\w{0,10})/$', 'ratings4you.views_admin.themes'),
   (r'^admin/catalogs/regions/(?P<id>\w{0,10})/$', 'ratings4you.views_admin.regions'),
   
   (r'^admin/moderation/$', 'ratings4you.views_admin.moderation'),
   (r'^admin/moderaterating/(?P<id>\w{0,10})/$', 
    'ratings4you.views_admin.moderate_rating'),
   (r'^admin/rating_send_mail$', 'ratings4you.views_admin.rating_send_mail'),
   (r'^admin/moderator_email/$', 'ratings4you.views_admin.moderator_email'),
   (r'^admin/edit_unmoderated_items/(?P<id>\w{0,10})/$', 'ratings4you.views_admin.edit_unmoderated_items'),
   (r'^admin/catalogs/themes/edit/(?P<id>\w{0,10})/$',
    'ratings4you.views_admin.edit_theme_item'),                        
   (r'^admin/catalogs/regions/edit/(?P<id>\w{0,10})/$',
    'ratings4you.views_admin.edit_region_item'),
)