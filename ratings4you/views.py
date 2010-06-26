# -*- coding: utf8 -*-
# Create your views here.
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from forms import RatingModelForm
from models import Rating
from db_rating import *

def index(request):
    #ratings = listActualRatings()
    ratings = Rating.objects.all()
    return render_to_response('ratings/index.html', dict (ratings=ratings),
                              context_instance=RequestContext(request))
    
def add(request):
    """
    метод добавления рейтинга
    """
    if request.POST:
        form = RatingModelForm(data=request.POST)
        if (form.is_valid()):
            entity = form.save()
            entity.author = request.user
            entity.save()
        else:
            return render_to_response('ratings/one_form_page.html', dict(form=form, link="/ratings/", link_text="или просто продолжайте сёрфинг с главной"),
                              context_instance=RequestContext(request))
    form = RatingModelForm()
    return render_to_response('ratings/one_form_page.html', dict(form=form, link="/ratings/", link_text="или просто продолжайте серфинг с главной"),
                              context_instance=RequestContext(request))
