# -*- coding: utf8 -*-
'''
Created on 25.06.2010

@author: alarin
'''
import django
from django import forms
from django.forms import ModelForm, DateField
from models import Rating, RatingThemesDirectory, RegionDirectory, RatingItem
from captcha.fields import CaptchaField

def customize_date_fields(f):
    if isinstance(f, django.db.models.fields.DateField):
        date_field=DateField(widget=forms.DateInput(format='%d.%m.%Y'), label=f.verbose_name)
        date_field.input_formats = ("%d.%m.%Y",)# + (date_field.input_formats)
        return date_field
    else:
        return f.formfield()


class RatingModelForm(ModelForm):
    """
    форма создания/редактирования 
    """
    formfield_callback = customize_date_fields
    
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
    
