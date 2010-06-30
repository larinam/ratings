# -*- coding: utf8 -*-
# Create your views here.
from db_rating import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from forms import RatingModelForm, RatingItemForm
from models import Rating, RatingItem

def index(request):
    #ratings = listActualRatings()
    ratings = Rating.objects.all()
    return render_to_response('ratings/index.html', dict (ratings=ratings),
                              context_instance=RequestContext(request))


@login_required
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
            return render_to_response('ratings/one_form_page.html', dict(form=form, link="/ratings/", title="Добавление рейтинга", link_text="или просто продолжайте сёрфинг с главной"),
                              context_instance=RequestContext(request))
    form = RatingModelForm()
    return render_to_response('ratings/one_form_page.html', dict(form=form, link="/ratings/", title="Добавление рейтинга", link_text="или просто продолжайте серфинг с главной"),
                              context_instance=RequestContext(request))

@login_required
def add_item(request, id):
    '''
    добавление элемента рейтинга
    '''
    rating = get_object_or_404(Rating, pk=id)
    rating_items = rating.listRatingItems()
    title = "Добавление элемента голосования для рейтинга %s" % (rating)
    if request.POST:
        form = RatingItemForm(data=request.POST)
        if form.is_valid():
            rating_item = rating.addRatingItem(name=form.cleaned_data['name'], author=request.user)
        else:
            return render_to_response('ratings/simple_catalogs_management.html', 
                                      dict(form=form, title=title, link="/ratings/", link_text="или просто продолжайте серфинг с главной",
                                           catalog_items=rating_items),
                              context_instance=RequestContext(request))
    form = RatingItemForm()
    return render_to_response('ratings/simple_catalogs_management.html', 
                              dict(form=form, title=title, link="/ratings/", link_text="или просто продолжайте серфинг с главной",
                                   catalog_items=rating_items),
                              context_instance=RequestContext(request))

def view_rating(request, id):
    '''
    отображение рейтинга для голосования
    '''
    rating = get_object_or_404(Rating, pk=id)
    if request.POST:
        rating_item_id = request.POST.get('ri_id')
        rating_item = get_object_or_404(RatingItem, pk=rating_item_id)
        rating_item.addVote(request.user, request.META['REMOTE_ADDR'])
        return render_to_response('ratings/rating_results.html', dict(title=rating.name, rating=rating, rating_items=rating.listRatingItems(), link="/ratings/", link_text="или просто продолжайте серфинг с главной"),
                              context_instance=RequestContext(request))
    if request.GET.get('action') == 'view_results':
        return render_to_response('ratings/rating_results.html', dict(title=rating.name, rating=rating, rating_items=rating.listRatingItems(), link="/ratings/view/%s/" % (rating.id), link_text="или вернитесь на страничку голосования"),
                              context_instance=RequestContext(request))
    return render_to_response('ratings/rating_poll.html', dict(title=rating.name, rating=rating, rating_items=rating.listRatingItems(), link="/ratings/", link_text="или просто продолжайте серфинг с главной"),
                              context_instance=RequestContext(request))
