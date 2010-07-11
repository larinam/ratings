# -*- coding: utf8 -*-
'''
Created on 25.06.2010

@author: alarin
'''
from django import forms
from django.forms import ModelForm
from models import Rating, RatingThemesDirectory, RegionDirectory, RatingItem
from captcha.fields import CaptchaField

class RatingModelForm(ModelForm):
    class Meta:
        model = Rating
        exclude = ['moderated', 'author']
        
class RatingThemesDirectoryForm(ModelForm):
    class Meta:
        model = RatingThemesDirectory
        
        
class RegionDirectoryForm(ModelForm):
    class Meta:
        model = RegionDirectory
        
class RatingItemForm(ModelForm):
    class Meta:
        model = RatingItem
        exclude = ['moderated', 'author', 'rating']
        
        
class FeedbackForm(forms.Form):
    '''
    Форма обратной связи.
    '''
    name = forms.CharField(label="Имя", required=True)
    contacts = forms.CharField(label="Контактные данные", required=True)
    question = forms.CharField(label="Содержание", widget=forms.Textarea, required=True)
    captcha = CaptchaField()
    
class SendMailForm(forms.Form):
    rating_id = forms.IntegerField(required=True, widget=forms.HiddenInput())
    subject = forms.CharField(label="Тема письма", required=True)
    body = forms.CharField(label="Текст письма", required=True, widget=forms.Textarea)
    
