# -*- coding: utf8 -*-
# Create your views here.
from db_rating import *
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from forms import RatingModelForm, RatingItemForm
from models import Rating

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
            return HttpResponseRedirect(reverse('ratings.ratings4you.views.add_item', kwargs=dict(id=entity.id)))
        else:
            return render_to_response('ratings/one_form_page.html', dict(form=form, link="/ratings/", link_text="или просто продолжайте сёрфинг с главной"),
                              context_instance=RequestContext(request))
    form = RatingModelForm()
    return render_to_response('ratings/one_form_page.html', dict(form=form, link="/ratings/", link_text="или просто продолжайте серфинг с главной"),
                              context_instance=RequestContext(request))

def add_item(request, id):
    '''
    добавление элемента рейтинга
    '''
    rating = get_object_or_404(Rating, pk=id)
    title = "Добавление элемента голосования для рейтинга %s" % (rating)
    if request.POST:
        form = RatingItemForm(data=request.POST)
        if form.is_valid():
            entity = form.save()
            entity.author = request.user
            entity.rating = rating
            entity.save()
        else:
            return render_to_response('ratings/one_form_page.html', dict(form=form, title=title, link="/ratings/", link_text="или просто продолжайте серфинг с главной"),
                              context_instance=RequestContext(request))
    form = RatingItemForm()
    return render_to_response('ratings/one_form_page.html', dict(form=form, title=title, link="/ratings/", link_text="или просто продолжайте серфинг с главной"),
                              context_instance=RequestContext(request))
    
def view_rating(request, id):
    '''
    отображение рейтинга для голосования
    '''
    rating = get_object_or_404(Rating, pk=id)
    return render_to_response('ratings/rating_poll.html', dict(title=rating.name, rating_items=rating.listRatingItems(), link="/ratings/", link_text="или просто продолжайте серфинг с главной"),
                              context_instance=RequestContext(request))
