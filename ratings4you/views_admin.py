# -*- coding: utf8 -*-
# Create your views here.
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from forms import RatingModelForm, RatingThemesDirectoryForm, RegionDirectoryForm
from models import RegionDirectory, RatingThemesDirectory


def index(request):
    return render_to_response('ratings/index_admin.html',
                              context_instance=RequestContext(request))
    
def catalogs(request):
    return render_to_response('ratings/admin/catalogs_admin.html',
                              context_instance=RequestContext(request))
    
def themes(request):
    if request.POST:
        data_dict = request.POST
        form = RatingThemesDirectoryForm(data=data_dict)
        if (form.is_valid()):
            entity = form.save(commit=True)
        else:
            return render_to_response('ratings/one_form_page.html', dict(form=form, link="/ratings/admin/catalogs/", link_text="или вернитесь в список каталогов"),
                              context_instance=RequestContext(request))
    form = RatingThemesDirectoryForm()
    return render_to_response('ratings/one_form_page.html', dict(form=form, link="/ratings/admin/catalogs/", link_text="или вернитесь в список каталогов"),
                              context_instance=RequestContext(request))

def regions(request):
    if request.POST:
        data_dict = request.POST
        form = RegionDirectoryForm(data=data_dict)
        if (form.is_valid()):
            entity = form.save(commit=True)
        else:
            return render_to_response('ratings/one_form_page.html', dict(form=form, link="/ratings/admin/catalogs/", link_text="или вернитесь в список каталогов"),
                              context_instance=RequestContext(request))
    form = RegionDirectoryForm()
    return render_to_response('ratings/one_form_page.html', dict(form=form, link="/ratings/admin/catalogs/", link_text="или вернитесь в список каталогов"),
                              context_instance=RequestContext(request))

    
#def add(request):
#    form = RatingModelForm()
#    return render_to_response('ratings/one_form_page.html', dict(form=form, link="/", link_text="или просто продолжайте серфинг с главной"),
#                              context_instance=RequestContext(request))
