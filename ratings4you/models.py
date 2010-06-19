from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from interfaces import IModeratable

# Create your models here.

# 
class UserProfile(models.Model):
    juridical_name = models.CharField(max_length=255, help_text="Название юридического лица") #Название организации
    contact_person = models.CharField(max_length=255, help_text="Контактное лицо") #Контактное лицо
    inn = models.CharField(max_length=255, help_text="ИНН")
    address = models.TextField(help_text="Адрес")
    phone_numer = models.CharField(max_length=255, help_text="Номер телефона")
    user = models.ForeignKey(User, unique=True)
    
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

class  Rating(models.Model, IModeratable):
    """
    Сам рейтинг, содержащий пункты для голосования.
    Один из главных бизнес-объектов.
    """
    name = models.CharField()
    region = models.ForeignKey(RegionDirectory, unique=True)
    theme = models.ForeignKey(RatingThemesDirectory, unique=True)
    begin_date = models.DateField()
    end_date = models.DateField()
    moderated = models.BooleanField(default=False)
    
    def addRatingItem(self, name):
        rating_item = RatingItem(name=name, rating=self)
        rating_item.save()
        return rating_item
        
    def listRatingItems(self):
        return RatingItem.objects.filter(rating=self)
    
    def isModerated(self):
        return moderated
    
    def setModerated(self, value=True):
        self.moderated = value

    
class RatingItem(models.Model, IModeratable):
    """
    Пункт рейтинга в @see: Rating .
    Один из главных бизнес-объектов.
    """
    name = models.CharField()
    rating = models.ForeignKey(Rating, unique=True)
    moderated = models.BooleanField(default=False)
    
    def addVote(self, user, ip):
        vote = Vote(user=user, rating_item=self, ip=ip)
        vote.save()
        
    def isModerated(self):
        return moderated
        
    def setModerated(self, value=True):
        self.moderated = value

class Vote(models.Model):
    """
    Голос, отданный за тот или иной пункт рейтинга. @see: RatingItem
    Один из главных бизнес-объектов.
    Не должно быть возможности как-то изменить.
    """
    user = models.ForeignKey(User, unique=True)
    vote_date = models.DateTimeField(auto_now=True)
    rating_item = models.ForeignKey(RatingItem, unique=True)
    ip = models.IPAddressField()
    