from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# 
class RatingThemesDirectory(models.Model):
    """
    Справочник тем для голосований.
    """
    name = models.CharField()

class RegionDirectory(models.Model):
    """
    Справочник регионов - здесь могут быть как страны, города, области, так и всё что угодно.
    """
    name = models.CharField()

class  Rating(models.Model):
    """
    Сам рейтинг, содержащий пункты для голосования.
    """
    name = models.CharField()
    region = models.ForeignKey(RegionDirectory, unique=True)
    theme = models.ForeignKey(RatingThemesDirectory, unique=True)
    begin_date = models.DateField()
    end_date = models.DateField()
    
    
class RatingItem(models.Model):
    """
    Пункт рейтинга в @see: Rating .
    """
    name = models.CharField()
    rating = models.ForeignKey(Rating, unique=True)

class Vote(models.Model):
    """
    Голос, отданный за тот или иной пункт рейтинга. @see: RatingItem
    """
    user = models.ForeignKey(User, unique=True)
    vote_date = models.DateTimeField(auto_now=True)
    rating_item = models.ForeignKey(RatingItem, unique=True)
    ip = models.IPAddressField()
    