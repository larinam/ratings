'''
Created on 03.01.2010

@author: alarin
'''

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from models import UserProfile
from views import getVotedFromSession, setSessionVoted


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'profile_url', 'authorization_mode']

@login_required
def profile(request):
    user = request.user
    if user.is_superuser:
        return HttpResponseRedirect(reverse('ratings4you.views_admin.index'))
    p = user.get_profile()
    if request.method == 'POST':
        f = UserProfileForm(request.POST, instance=p)
        if f.is_valid():
            print "everything is valid"
            f.save()
            
    else:
        f = UserProfileForm(instance=p)
    return render_to_response('ratings/profile_form_page.html', dict(widget=f, profile=p),
                                              context_instance=RequestContext(request))
         
def logout_view(request):
    voted = getVotedFromSession(request.session)
    logout(request)
    setSessionVoted(request.session, voted)
    response = redirect('ratings4you.views.index')
    return response
    

