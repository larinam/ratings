'''
Created on 03.01.2010

@author: alarin
'''

from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from models import UserProfile

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        
def profile(request):
    if request.method == 'POST':
        f = UserProfileForm(request.POST, instance=request.user.get_profile())
        if f.is_valid():
            print "everything is valid"
            f.save()
            
    else:
        
        user = request.user
        p = user.get_profile()
        f = UserProfileForm(instance=p)
    return render_to_response('ratings/profile_form_page.html', dict(widget=f),
                                              context_instance=RequestContext(request))
         

