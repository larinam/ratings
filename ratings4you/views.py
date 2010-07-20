# -*- coding: utf8 -*-
# Create your views here.
from db_rating import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from forms import FeedbackForm, RatingModelForm, RatingItemForm
from models import Rating, RatingItem
from settings import PROJECT_URL_BASE
from views_admin import TO_EMAIL

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
    link_text="или просто продолжайте серфинг с главной"
    link = "/ratings/"
    if request.POST:
        form = RatingItemForm(data=request.POST)
        if form.is_valid():
            rating_item = rating.addRatingItem(name=form.cleaned_data['name'], author=request.user)
            link_text="или отправьте рейтинг на премодерацию"
            link = "/ratings/sendtomoder/%d/" % (rating.id)
        else:
            return render_to_response('ratings/simple_catalogs_management.html', 
                                      dict(form=form, title=title, link="/ratings/", link_text="или просто продолжайте серфинг с главной",
                                           catalog_items=rating_items),
                              context_instance=RequestContext(request))
    form = RatingItemForm()
    return render_to_response('ratings/simple_catalogs_management.html', 
                              dict(form=form, title=title, link=link, link_text=link_text,
                                   catalog_items=rating_items),
                              context_instance=RequestContext(request))

def send_to_moderator(request, id):
    """
    Отправить письмо модератору о том, что рейтинг добавлен и нужно его отмодерировать
    """
    rating = get_object_or_404(Rating, pk=id)
    send_mail("Рейтинг добавлен и ожидает модерации", PROJECT_URL_BASE+"/ratings/admin/moderaterating/"+str(rating.id)+"/", request.user.email, [TO_EMAIL])
    return render_to_response('ratings/message.html', 
                              dict(title="Рейтинг добавлен и ожидает модерации", link='/ratings/', link_text='на главную'),
                              context_instance=RequestContext(request))
    
def view_rating(request, id):
    '''
    отображение рейтинга для голосования и нажатие кнопки голосовать
    '''
    user = request.user
    rating = get_object_or_404(Rating, pk=id)
    userVoted = rating.userVoted(user)
    if request.POST and not userVoted:
        rating_item_id = request.POST.get('ri_id')
        if rating_item_id:
            rating_item = get_object_or_404(RatingItem, pk=rating_item_id)
            rating_item.addVote(request.user, request.META['REMOTE_ADDR'])
            return render_to_response('ratings/rating_results.html', 
                                      dict(title=rating.name, rating=rating, 
                                           rating_items=rating.listModeratedRatingItems(), 
                                           link="/ratings/", 
                                           link_text="или просто продолжайте серфинг с главной"),
                                  context_instance=RequestContext(request))

    if request.GET.get('action') == 'view_results' or not user.is_authenticated() or userVoted:
        return render_to_response('ratings/rating_results.html', dict(title=rating.name, rating=rating, rating_items=rating.listModeratedRatingItems(), link="/ratings/view/%s/" % (rating.id), link_text="или вернитесь на страничку голосования"),
                              context_instance=RequestContext(request))
    return render_to_response('ratings/rating_poll.html', dict(title=rating.name, rating=rating, rating_items=rating.listModeratedRatingItems(), link="/ratings/", link_text="или просто продолжайте серфинг с главной"),
                              context_instance=RequestContext(request))


def feedback(request):
    if request.POST:
        form = FeedbackForm(request.POST.copy())
        if not form.is_valid():
            return render_to_response("metal/one_form_page.html", dict(widget=form))
        data = form.cleaned_data
        send_mail("Письмо с сайта", data["question"], "larinam@gmail.com", ["larinam@gmail.com"], False, "", "")
        return render_to_response("metal/one_widget_page.html", dict(widget="Спасибо за обратную связь!", link="/", link_text="Вернуться на главную."),
                              context_instance=RequestContext(request))
    form = FeedbackForm()
    return render_to_response("metal/one_form_page.html", dict(widget=form, link="mailto:krater@narod.ru", link_text="или напишите нам через почтовый клиент"),
                              context_instance=RequestContext(request))
