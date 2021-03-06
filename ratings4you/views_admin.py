# -*- coding: utf8 -*-
# Create your views here.
from db_rating import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from forms import FeedbackForm, RatingModelForm, RatingThemesDirectoryForm, \
    RegionDirectoryForm, RatingItemForm, SendMailForm, EditModeratorEmailForm
from models import RegionDirectory, RatingThemesDirectory, MODERATABLE_MODELS
from ratings4you.models import RatingItem, KVTable

FROM_EMAIL = KVTable.objects.get_or_create(key_column="moderator_email")[0].value_column or "krater@narod.ru"
TO_EMAIL = 'krater@narod.ru'


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render_to_response('ratings/index_admin.html',
                              context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_superuser)
def catalogs(request):
    return render_to_response('ratings/admin/catalogs_admin.html',
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def themes(request, id=None):
    if id:
        catalog_items = RatingThemesDirectory.objects.filter(parent=id).order_by('name')
    else:
        catalog_items = RatingThemesDirectory.objects.filter(parent=None).order_by('name')
        id = ""
    if request.POST:
        data_dict = request.POST
        form = RatingThemesDirectoryForm(data=data_dict)
        if (form.is_valid()):
            entity = form.save(commit=True)
            if id:
                entity.setParent(RatingThemesDirectory.objects.get(pk=id))
        else:
            return render_to_response('ratings/simple_catalogs_management.html',
                                      dict(form=form, link="/ratings/admin/catalogs/", title="Темы голосований",
                                           link_text="Вернуться в список каталогов", catalog_items=catalog_items),
                              context_instance=RequestContext(request))
    form = RatingThemesDirectoryForm()
    return render_to_response('ratings/simple_catalogs_management.html',
                              dict(form=form, link="/ratings/admin/catalogs/", title="Темы голосований",
                                   link_text="Вернуться в список каталогов", catalog_items=catalog_items),
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def regions(request, id=None):
    if id:
        catalog_items = RegionDirectory.objects.filter(parent=id).order_by('name')
    else:
        catalog_items = RegionDirectory.objects.filter(parent=None).order_by('name')
        id = ""
    if request.POST:
        data_dict = request.POST
        form = RegionDirectoryForm(data=data_dict)
        if (form.is_valid()):
            entity = form.save(commit=True)
            if id:
                entity.setParent(RegionDirectory.objects.get(pk=id))
        else:
            return render_to_response('ratings/simple_catalogs_management.html',
                                      dict(form=form,
                                           title="Регионы голосований",
                                           link="/ratings/admin/catalogs/",
                                           link_text="Вернуться в список каталогов",
                                           catalog_items=catalog_items, parent=id),
                              context_instance=RequestContext(request))
    form = RegionDirectoryForm()
    return render_to_response('ratings/simple_catalogs_management.html',
                              dict(form=form,
                                   title="Регионы голосований",
                                   link="/ratings/admin/catalogs/",
                                   link_text="Вернуться в список каталогов",
                                   catalog_items=catalog_items, parent=id),
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def moderation(request):
    moderatable = Rating.objects.filter() #listActualRatings()
    return render_to_response('ratings/admin/moderation_admin.html',
                              dict(moderatable=moderatable,
                                   title="Модерация",
                                   link="/ratings/admin/",
                                   link_text="Вернуться в раздел администрирование",
                                   ),
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def moderate_rating(request, id):
    rating = Rating.objects.get(pk=id)
    moderatable = rating.listRatingItems()
    isRatingModerated = False
    isModeratableModerated = {}
    for i in moderatable:
        isModeratableModerated.update({i.id:False})
    if request.POST:
        if 'delete' in request.POST.keys():
            rating.delete()
            return HttpResponseRedirect(reverse('ratings4you.views_admin.moderation'))
        for i in request.POST:
            if i.startswith('rating') and i.replace('rating', '') == id and request.POST.get(i) == 'on':
                isRatingModerated = True
            elif i.startswith('ratingitem') and request.POST.get(i) == 'on':
                mId = i.replace('ratingitem', '')
                isModeratableModerated.update({int(mId):True})
        rating.setModerated(value=isRatingModerated)
        for i in moderatable:
            i.setModerated(value=isModeratableModerated.get(i.id))
        return HttpResponseRedirect(reverse('ratings4you.views_admin.moderation'))
    send_mail_form = SendMailForm(initial=dict(rating_id=id))
    return render_to_response('ratings/admin/moderate_rating_admin.html',
                              dict(rating=rating, moderatable=moderatable,
                                   send_mail_form=send_mail_form,
                                   title="Модерация рейтинга",
                                   link="/ratings/admin/moderation/",
                                   link_text="Вернуться к списку модерируемых рейтингов",
                                   ),
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def edit_unmoderated_items(request, id):
    rating = get_object_or_404(Rating, pk=id)
    if request.POST:
        for i in request.POST:
            if i.startswith('ri'):
                riid = i.replace('ri', '')
                ratingItem = get_object_or_404(RatingItem, pk=riid)
                ratingItem.setName(request.POST.get(i))
        return HttpResponseRedirect(reverse('ratings4you.views_admin.moderate_rating', kwargs={"id":rating.id}))
    unmoderated = rating.listUnmoderatedRatingItems()
    return render_to_response('ratings/admin/edit_rating_admin.html',
                              dict(rating=rating, unmoderated=unmoderated,
                                   title="Редактирование рейтинга",
                                   link="/ratings/admin/moderaterating/%d/" % rating.id,
                                   link_text="Вернуться к модерированию рейтинга",
                                   ),
                              context_instance=RequestContext(request))
    

@user_passes_test(lambda u: u.is_superuser)
def rating_send_mail(request):
    if request.POST:
        form = SendMailForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            rating_id = data.get('rating_id')
            rating = Rating.objects.get(pk=rating_id)
            subject = data.get('subject')
            body = data.get('body')
            
            rating.author.email_user(subject, body, FROM_EMAIL)
            #to_email = rating.author.email
            #send_mail(subject, body, FROM_EMAIL, [TO_EMAIL], False, "", "")
            return HttpResponseRedirect(reverse('ratings4you.views_admin.moderate_rating', kwargs={"id":rating_id}))

@user_passes_test(lambda u: u.is_superuser)
def moderator_email(request):
    moderator_email = KVTable.objects.get_or_create(key_column="moderator_email")[0]
    form = EditModeratorEmailForm(initial={"email":moderator_email.value_column})
    if request.POST:
        form = EditModeratorEmailForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = data.get('email')
            moderator_email.value_column = email
            moderator_email.save()
    return render_to_response("ratings/one_form_page.html", dict(form=form, link="/ratings/admin/", link_text="Вернуться в раздел администрирование",
                                                                 title="Редактирование e-mail администратора"),
                              context_instance=RequestContext(request))
    
@user_passes_test(lambda u: u.is_superuser)
def edit_theme_item(request, id):
    theme = get_object_or_404(RatingThemesDirectory, pk=id)
    if request.POST:
        data_dict = request.POST
        form = RatingThemesDirectoryForm(data_dict, instance=theme)
        if (form.is_valid()):
            entity = form.save(commit=True)
            return HttpResponseRedirect(reverse('ratings4you.views_admin.themes'))
        else:
            return render_to_response('ratings/admin/edit_simple_catalog_item.html',
                                      dict(form=form, link="/ratings/admin/catalogs/themes/", title="Редактирование темы голосований",
                                           link_text="Вернуться в список тем"),
                              context_instance=RequestContext(request))
    form = RatingThemesDirectoryForm(instance=theme)
    return render_to_response('ratings/admin/edit_simple_catalog_item.html',
                              dict(form=form, link="/ratings/admin/catalogs/themes/", title="Редактирование темы голосований",
                                   link_text="Вернуться в список тем"),
                              context_instance=RequestContext(request))
    
@user_passes_test(lambda u: u.is_superuser)
def edit_region_item(request, id):
    region = get_object_or_404(RegionDirectory, pk=id)
    if request.POST:
        data_dict = request.POST
        form = RegionDirectoryForm(data_dict, instance=region)
        if (form.is_valid()):
            entity = form.save(commit=True)
            return HttpResponseRedirect(reverse('ratings4you.views_admin.regions'))
        else:
            return render_to_response('ratings/admin/edit_simple_catalog_item.html',
                                      dict(form=form, link="/ratings/admin/catalogs/regions/", title="Редактирование региона",
                                           link_text="Вернуться в список регионов"),
                              context_instance=RequestContext(request))
    form = RatingThemesDirectoryForm(instance=region)
    return render_to_response('ratings/admin/edit_simple_catalog_item.html',
                              dict(form=form, link="/ratings/admin/catalogs/regions/", title="Редактирование региона",
                                   link_text="Вернуться в список регионов"),
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def delete_region_item(request, id):
    kwargs={}
    region = get_object_or_404(RegionDirectory, pk=id)
    p = region.parent
    if p:
        kwargs={"id":p.id}
    region.delete()
    return HttpResponseRedirect(reverse('ratings4you.views_admin.regions', kwargs=kwargs))
    
@user_passes_test(lambda u: u.is_superuser)
def delete_theme_item(request, id):
    kwargs={}
    theme = get_object_or_404(RatingThemesDirectory, pk=id)
    p = theme.parent
    if p:
        kwargs={"id":p.id}
    theme.delete()
    return HttpResponseRedirect(reverse('ratings4you.views_admin.themes', kwargs=kwargs))
#def add(request):
#    form = RatingModelForm()
#    return render_to_response('ratings/one_form_page.html', dict(form=form, link="/", link_text="или просто продолжайте серфинг с главной"),
#                              context_instance=RequestContext(request))
