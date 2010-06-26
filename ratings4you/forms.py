'''
Created on 25.06.2010

@author: alarin
'''
from django.forms import ModelForm
from models import Rating, RatingThemesDirectory, RegionDirectory

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