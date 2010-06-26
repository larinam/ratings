#!/usr/bin/python
# -*- coding: utf8 -*-
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from interfaces import IModeratable, NameAsIdentifier

# Create your models here.

# 
AUTHORIZATION_CHOICES = (
    ('Anonymous', 'Анонимный'),
    ('Authorized', 'Авторизованный'),
)

BONUS_CHOICES = (
    ('RUR', 'Рубль'),
    ('USD', 'Американский доллар'),
    ('EUR', 'Евро'),
)

class UserProfile(models.Model):
    authorization_mode = models.CharField(max_length=255, choices=AUTHORIZATION_CHOICES)
    bonus_currency = models.CharField(max_length=255, choices=BONUS_CHOICES)
    user = models.ForeignKey(User, unique=True)
    
def create_user_profile(sender, instance, created, **kwargs):  
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User) 
    
class RatingThemesDirectory(models.Model, NameAsIdentifier):
    """
    Справочник тем для голосований.
    """
    name = models.CharField(max_length=255, unique=True, null=False, help_text="Тема голосования")

class RegionDirectory(models.Model, NameAsIdentifier):
    """
    Справочник регионов - здесь могут быть как страны, города, области, так и всё что угодно.
    """
    name = models.CharField(max_length=255, unique=True, null=False, verbose_name="Регион", help_text="Регион, для которого проводится голосование")

class  Rating(models.Model, IModeratable, NameAsIdentifier):
    """
    Сам рейтинг, содержащий пункты для голосования.
    Один из главных бизнес-объектов.
    """
    name = models.CharField(max_length=255, help_text="Название рейтинга")
    region = models.ForeignKey(RegionDirectory, help_text="Регион")
    theme = models.ForeignKey(RatingThemesDirectory, help_text="Тема рейтинга")
    begin_date = models.DateField(verbose_name="Дата начала голосования", help_text="Дата начала голосования")
    end_date = models.DateField(verbose_name="Дата окончания голосования", help_text="Дата окончания голосования")
    moderated = models.BooleanField(default=False, help_text="Прошёл модерацию")
    author = models.ForeignKey(User, null=True) # автор рейтинга
    
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

    
class RatingItem(models.Model, IModeratable, NameAsIdentifier):
    """
    Пункт рейтинга в @see: Rating .
    Один из главных бизнес-объектов.
    """
    name = models.CharField(max_length=255, verbose_name="Название элемента голосования", help_text="Название пункта голосования")
    rating = models.ForeignKey(Rating, unique=True)
    moderated = models.BooleanField(default=False)
    author = models.ForeignKey(User, null=True) # автор изменений внесенных в элемент
    
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
    user = models.ForeignKey(User)
    vote_date = models.DateTimeField(auto_now=True)
    rating_item = models.ForeignKey(RatingItem)
    ip = models.IPAddressField()
    