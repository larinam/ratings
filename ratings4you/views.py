# -*- coding: utf8 -*-
# Create your views here.
from db_rating import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from forms import FeedbackForm, RatingModelForm, RatingItemForm
from models import Rating, RatingItem, RatingThemesDirectory, RegionDirectory, \
    User
from recaptcha.librecaptcha import displayhtml, submit
from settings import DEFAULT_FROM_EMAIL, PROJECT_URL_BASE
from views_admin import TO_EMAIL
ELEMENTS_TO_ADD_COUNT = 10

def getCaptcha(error=None):
    return displayhtml('6Lfe9b4SAAAAAPvGjMLShAO9lTkjBtQT6N_MP_uQ', error=error, theme='white')

def checkCaptcha(request):
    return submit(request.POST.get('recaptcha_challenge_field',''),
            request.POST.get('recaptcha_response_field',''),
            '6Lfe9b4SAAAAAFTHt3cRiSYsaf0D-4H3_ta7EG4D',
            request.META.get('REMOTE_ADDR', None))

def setSessionVoted(session, id):
    voted = session.get("voted", [])
    if type(id) == type([]):
        voted.extend(id)
    else:
        voted.append(id)
    session.update({"voted":voted})
    return session

def getVotedFromSession(session):
    return session.get("voted", [])

def index(request):
    #ratings = listActualRatings()
    ratings = listTopRatings()
    return render_to_response('ratings/index.html', dict (ratings=ratings, title="Популярные рейтинги"),
                              context_instance=RequestContext(request))

@login_required
def add(request):
    """
    метод добавления рейтинга
    """
    form = RatingModelForm()
    if request.POST:
        form = RatingModelForm(data=request.POST)
        if (form.is_valid()):
            entity = form.save()
            entity.author = request.user
            entity.save()
            return HttpResponseRedirect(reverse('ratings4you.views.add_item', kwargs=dict(id=entity.id)))

    return render_to_response('ratings/one_form_page.html', dict(form=form, link="/ratings/", title="Создание рейтинга", link_text=""),
                              context_instance=RequestContext(request))

@login_required
def add_item(request, id):
    '''
    добавление элемента рейтинга
    '''
    user = request.user
    rating = get_object_or_404(Rating, pk=id)
    if user != rating.author:
        return HttpResponseRedirect(reverse('ratings4you.views.view_rating', kwargs=dict(id=id))) #вернуть страничку с просмотром рейтинга вместо добавления элемента
    rating_items = rating.listRatingItems()
    title = 'Создание рейтинга'
    link_text=""
    link = "/ratings/"
    if request.POST:
        forms = [RatingItemForm(request.POST, prefix=str(x), instance=RatingItem()) for x in range(0,ELEMENTS_TO_ADD_COUNT)]
        if all([(form.is_valid()) for form in forms]):
            [rating.addRatingItem(name=form.cleaned_data['name'], author=user) for form in forms if form.cleaned_data['name']]
            link_text="Отправить рейтинг на премодерацию"
            link = "/ratings/sendtomoder/%d/" % (rating.id)
        else:
            return render_to_response('ratings/simple_catalogs_management_multiple.html', 
                                      dict(forms=forms, title=title, link="/ratings/", link_text="",
                                           catalog_items=rating_items),
                              context_instance=RequestContext(request))
    forms = [RatingItemForm(prefix=str(x), instance=RatingItem()) for x in range(0,ELEMENTS_TO_ADD_COUNT)]
    return render_to_response('ratings/simple_catalogs_management_multiple.html', 
                              dict(forms=forms, title=title, link=link, link_text=link_text,
                                   catalog_items=rating_items),
                              context_instance=RequestContext(request))

@login_required
def send_to_moderator(request, id):
    """
    Отправить письмо модератору о том, что рейтинг добавлен и нужно его отмодерировать
    """
    rating = get_object_or_404(Rating, pk=id)
    send_mail("Рейтинг добавлен и ожидает модерации", PROJECT_URL_BASE+"/ratings/admin/moderaterating/"+str(rating.id)+"/", request.user.email, [TO_EMAIL])
    return render_to_response('ratings/message.html', 
                              dict(title="Создание рейтинга", link='/ratings/', link_text='на главную', msg="Рейтинг создан и ожидает одобрения модератора"),
                              context_instance=RequestContext(request))
    
def view_rating(request, id):
    '''
    отображение рейтинга для голосования и нажатие кнопки голосовать
    '''
    error=None
    user = request.user
    rating = get_object_or_404(Rating, pk=id)
    userVoted = rating.userVoted(user) or (isinstance(request.user, AnonymousUser) and id in request.session.get("voted",[]))
    if request.POST and not userVoted:
        cRes=checkCaptcha(request)
        if not cRes.is_valid and isinstance(request.user, AnonymousUser):
            error = cRes.error_code
        elif (cRes.is_valid or not isinstance(request.user, AnonymousUser)):
            rating_item_id = request.POST.get('ri_id')
            if rating_item_id:
                rating_item = get_object_or_404(RatingItem, pk=rating_item_id)
                fake_user = request.user
                if isinstance(request.user, AnonymousUser): fake_user = User.objects.get(pk=1)
                rating_item.addVote(fake_user, request.META['REMOTE_ADDR'])
                userVoted = True
                setSessionVoted(request.session, id)

    if userVoted: #not user.is_authenticated() or 
        return HttpResponseRedirect(reverse('ratings4you.views.view_rating_results', kwargs=dict(id=id)))
    return render_to_response('ratings/rating_poll.html', dict(title=rating.name, rating=rating, rating_items=rating.listModeratedRatingItems(), link="/ratings/", 
                                                               link_text="", reCaptcha=getCaptcha(error=error)),
                              context_instance=RequestContext(request))
    
def view_ratings_list(request, id):
    '''
    отображение списка рейтингов определённой категории
    '''
    user = request.user
    rating_theme = get_object_or_404(RatingThemesDirectory, pk=id)
    ratings = rating_theme.listRatings()
    return render_to_response('ratings/ratings_list.html', dict(title=rating_theme.name, rating_theme=rating_theme, ratings=ratings, link="/ratings/", 
                                                               link_text=""),
                              context_instance=RequestContext(request))


def view_rating_results(request, id):
    '''
    отображение результатов голосования. упорядоченных по рейтингу.
    '''
    user = request.user
    rating = get_object_or_404(Rating, pk=id)
    userVoted = rating.userVoted(user)
    
    if not user.is_authenticated() or userVoted:
        link_text = ""
        link="/ratings/"
    else:
        link_text = "Вернуться на страничку голосования"
        link="/ratings/view/%s/" % (rating.id)
        
    rating_items=rating.listModeratedRatingItems()
    items = [(item.getOverallCount(), item) for item in rating_items]
    items.sort()
    items.reverse()
    rating_items = [item[1] for item in items]
    return render_to_response('ratings/rating_results.html', dict(title=rating.name, rating=rating, 
                                                                  rating_items=rating_items,
                                                                  link=link, 
                                                                  link_text=link_text),
                          context_instance=RequestContext(request))

def feedback(request):
    if request.POST:
        form = FeedbackForm(request.POST.copy())
        if not form.is_valid():
            return render_to_response("ratings/one_form_page.html", dict(form=form), context_instance=RequestContext(request))
        data = form.cleaned_data
        send_mail("Письмо с сайта", data["question"] + '\r\n\r\n' + data["name"] + data["contacts"], DEFAULT_FROM_EMAIL, [TO_EMAIL], False, "", "")
        return render_to_response("ratings/one_widget_page.html", dict(widget="Спасибо за обратную связь!", link="/ratings/", link_text="Вернуться на главную",
                                                                      title="Обратная связь" ),
                              context_instance=RequestContext(request))
    form = FeedbackForm()
    return render_to_response("ratings/one_form_page.html", dict(form=form, link="mailto:%s" % (TO_EMAIL), link_text="Написать нам через почтовый клиент", 
                                                                 title="Форма обратной связи"),
                              context_instance=RequestContext(request))

def development_message(request):
    return render_to_response("ratings/message.html", dict(msg="Раздел в разработке", link="/ratings/", link_text="Вернуться на главную", 
                                                                 title="Раздел находится в разработке"),
                              context_instance=RequestContext(request))