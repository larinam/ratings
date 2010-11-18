#!/usr/bin/python
# -*- coding: utf8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from interfaces import IModeratable, NameAsIdentifier
from datetime import datetime

# Create your models here.

# 
AUTHORIZATION_CHOICES = (
    ('Anonymous', 'Анонимный'),
    ('Authorized', 'Авторизованный'),
    ('Expert', 'Эксперт'),
)

BONUS_CHOICES = (
    ('RUR', 'Рубль'),
    ('USD', 'Американский доллар'),
    ('EUR', 'Евро'),
)

class UserProfile(models.Model):
    authorization_mode = models.CharField(max_length=255, verbose_name="Тип пользователя",
                                          choices=AUTHORIZATION_CHOICES, default=AUTHORIZATION_CHOICES[1][0])
    bonus_currency = models.CharField(max_length=255, verbose_name="В какой валюте хотите получать бонусы?",
                                      choices=BONUS_CHOICES) # Валюта бонуса
    profile_url = models.URLField(verbose_name="URL", verify_exists=True, null=True)
    user = models.ForeignKey(User, unique=True)
    
def create_user_profile(sender, instance, created, **kwargs):  
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance)


#чтобы init миграция проходил без сучка без задоринки 
post_save.connect(create_user_profile, sender=User)

    
class RatingThemesDirectory(models.Model, NameAsIdentifier):
    """
    Справочник тем для голосований.
    """
    name = models.CharField(max_length=255, unique=True, null=False, verbose_name="Тема голосования", help_text="Тема голосования")
    parent = models.ForeignKey('self', null=True)
    class Meta:
        ordering = ('name',)
        
    def getEditURI(self):
        return "/ratings/admin/catalogs/themes/edit/" + str(self.id) + "/"
    
    def getDrillDownURI(self):
        return "/ratings/admin/catalogs/themes/"+ str(self.id) + "/"
    
    def setParent(self, parent):
        self.parent = parent
        self.save()
        
    def listSubElements(self):
        return RatingThemesDirectory.objects.filter(parent=self)
    
    def listRatings(self):
        return Rating.objects.filter(theme=self, moderated=True)
        

class RegionDirectory(models.Model, NameAsIdentifier):
    """
    Справочник регионов - здесь могут быть как страны, города, области, так и всё что угодно.
    """
    name = models.CharField(max_length=255, unique=True, null=False, verbose_name="Регион", help_text="Регион, для которого проводится голосование")
    parent = models.ForeignKey('self', null=True)
    class Meta:
        ordering = ('name',)
        
    def getEditURI(self):
        return "/ratings/admin/catalogs/regions/edit/" + str(self.id) + "/"
    
    def getDrillDownURI(self):
        return "/ratings/admin/catalogs/regions/"+ str(self.id) + "/"
    
    def setParent(self, parent):
        self.parent = parent
        self.save()
        
    def listSubElements(self):
        return RegionDirectory.objects.filter(parent=self)

class  Rating(models.Model, IModeratable, NameAsIdentifier):
    """
    Сам рейтинг, содержащий пункты для голосования.
    Один из главных бизнес-объектов.
    """
    name = models.CharField(max_length=255, verbose_name="Название рейтинга") #, help_text="Название рейтинга"
    region = models.ForeignKey(RegionDirectory, verbose_name="Регион") #, help_text="Регион"
    theme = models.ForeignKey(RatingThemesDirectory, verbose_name="Тема рейтинга") #, help_text="Тема рейтинга"
    begin_date = models.DateField(verbose_name="Дата начала голосования", help_text="например, 01.01.2010")
    end_date = models.DateField(verbose_name="Дата окончания голосования", help_text="например, 31.12.2010")
    moderated = models.BooleanField(default=False, help_text="Прошёл модерацию")
    author = models.ForeignKey(User, null=True) # автор рейтинга
    creation_date = models.DateTimeField(verbose_name="Дата создания голосования", auto_now=True, null=False, default=datetime.now())
    time_moderated = models.DateTimeField(verbose_name="Время, когда был принят для отображения пользователю", null=True)
    
    class Meta:
        ordering = ('name',)
    
    def addRatingItem(self, name, author):
        rating_item = RatingItem(name=name, rating=self, author=author)
        rating_item.save()
        return rating_item
        
    def listRatingItems(self):
        return RatingItem.objects.filter(rating=self)
    
    def listModeratedRatingItems(self):
        return RatingItem.objects.filter(rating=self, moderated=True)
    
    def listUnmoderatedRatingItems(self):
        return RatingItem.objects.filter(rating=self, moderated=False)
    
    def isModerated(self):
        return self.moderated
    
    def setModerated(self, value=True):
        if value:
            self.time_moderated = datetime.now()
        self.moderated = value
        self.save()
        
    def hasNotModeratedItems(self):
        """
        имеет неотмодерированные пункты голосования
        """
        return 0 != RatingItem.objects.filter(rating=self, moderated=False).count()
    
    def delete(self):
        for item in self.listRatingItems():
            item.delete()
        super(Rating, self).delete()
        
    def listVotes(self):
        votes = []
        for ri in self.listRatingItems():
            votes += list(Vote.objects.filter(rating_item=ri))
        return votes
    
    def votesCount(self):
        count = 0
        for ri in self.listRatingItems():
            count += Vote.objects.filter(rating_item=ri).count()
        return count
    
    def userVoted(self, user):
        result = False
        for i in self.listVotes():
            if user == i.user:
                result = True
                
        return result
    
    def listUsersVoted(self):
        return [i.user for i in self.listVotes()]
        

    
class RatingItem(models.Model, IModeratable, NameAsIdentifier):
    """
    Пункт рейтинга в @see: Rating .
    Один из главных бизнес-объектов.
    """
    name = models.CharField(max_length=255, verbose_name="Пункт рейтинга", help_text="")
    rating = models.ForeignKey(Rating)
    moderated = models.BooleanField(default=False)
    author = models.ForeignKey(User, null=True) # автор изменений внесенных в элемент
    creation_date = models.DateTimeField(verbose_name="Дата создания голосования", auto_now=True, null=False, default=datetime.now())
    time_moderated = models.DateTimeField(verbose_name="Время, когда был принят для отображения пользователю", null=True)
    
    class Meta:
        ordering = ('name',)
    
    def addVote(self, user, ip):
        vote = Vote(user=user, rating_item=self, ip=ip)
        vote.save()
        
    def isModerated(self):
        return self.moderated
        
    def setModerated(self, value=True):
        if value:
            self.time_moderated = datetime.now()
        self.moderated = value
        self.save()
        
    def getOverallCount(self):
        return Vote.objects.filter(rating_item=self).count()
    
    def getPercentage(self):
        return self.getOverallCount()/(self.rating.votesCount() or 1)*100
    
    def setName(self, value):
        self.name = value
        self.save()

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
    
class KVTable(models.Model):
    """
    Универсальное хранилище key-value таблица
    """
    key_column = models.CharField(max_length=255)
    value_column = models.CharField(max_length=255)

# Список моделей, реализующих интерфейс @see: IModeratable    
MODERATABLE_MODELS = (Rating, RatingItem)
