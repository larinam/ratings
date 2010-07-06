# -*- coding: utf8 -*-
# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from forms import RatingModelForm, RatingThemesDirectoryForm, \
    RegionDirectoryForm, RatingItemForm
from models import RegionDirectory, RatingThemesDirectory, MODERATABLE_MODELS
from db_rating import *


def index(request):
    return render_to_response('ratings/index_admin.html',
                              context_instance=RequestContext(request))
    
def catalogs(request):
    return render_to_response('ratings/admin/catalogs_admin.html',
                              context_instance=RequestContext(request))
    
def themes(request):
    catalog_items = RatingThemesDirectory.objects.all().order_by('name')
    if request.POST:
        data_dict = request.POST
        form = RatingThemesDirectoryForm(data=data_dict)
        if (form.is_valid()):
            entity = form.save(commit=True)
        else:
            return render_to_response('ratings/simple_catalogs_management.html', 
                                      dict(form=form, link="/ratings/admin/catalogs/", title="Темы голосований", 
                                           link_text="или вернитесь в список каталогов", catalog_items=catalog_items),
                              context_instance=RequestContext(request))
    form = RatingThemesDirectoryForm()
    return render_to_response('ratings/simple_catalogs_management.html', 
                              dict(form=form, link="/ratings/admin/catalogs/", title="Темы голосований",
                                   link_text="или вернитесь в список каталогов", catalog_items=catalog_items),
                              context_instance=RequestContext(request))

def regions(request):
    catalog_items = RegionDirectory.objects.all().order_by('name')
    if request.POST:
        data_dict = request.POST
        form = RegionDirectoryForm(data=data_dict)
        if (form.is_valid()):
            entity = form.save(commit=True)
        else:
            return render_to_response('ratings/simple_catalogs_management.html', 
                                      dict(form=form, 
                                           title="Регионы голосований",
                                           link="/ratings/admin/catalogs/", 
                                           link_text="или вернитесь в список каталогов",
                                           catalog_items=catalog_items),
                              context_instance=RequestContext(request))
    form = RegionDirectoryForm()
    return render_to_response('ratings/simple_catalogs_management.html', 
                              dict(form=form,
                                   title="Регионы голосований", 
                                   link="/ratings/admin/catalogs/",
                                   link_text="или вернитесь в список каталогов",
                                   catalog_items=catalog_items),
                              context_instance=RequestContext(request))

def moderation(request):
    moderatable = Rating.objects.filter() #listActualRatings()
    return render_to_response('ratings/admin/moderation_admin.html', 
                              dict(moderatable=moderatable,
                                   title="Модерация", 
                                   ),
                              context_instance=RequestContext(request))
    
def moderatie_rating(request, id):
    rating = Rating.objects.get(pk=id) #listActualRatings()
    moderatable = rating.listRatingItems()
    return render_to_response('ratings/admin/moderate_rating_admin.html', 
                              dict(rating=rating, moderatable=moderatable,
                                   title="Модерация рейтинга", 
                                   ),
                              context_instance=RequestContext(request))
        
        
    
#def add(request):
#    form = RatingModelForm()
#    return render_to_response('ratings/one_form_page.html', dict(form=form, link="/", link_text="или просто продолжайте серфинг с главной"),
#                              context_instance=RequestContext(request))
