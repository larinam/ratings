# -*- coding: utf8 -*-
'''
Created on 26.06.2010

@author: alarin
'''
from datetime import date
from models import Rating, RatingItem

def listTopRatingItems(lim=10):
    sql = """SELECT ratings4you_ratingitem.id, ratings4you_ratingitem.name, count(ratings4you_vote.id) as c 
            from ratings4you_vote, ratings4you_ratingitem 
            where ratings4you_vote.rating_item_id=ratings4you_ratingitem.id 
            group by ratings4you_vote.rating_item_id
            order by count(ratings4you_vote.id) desc"""
    ris = RatingItem.objects.raw(sql)[:lim]
    return ris

def listActualRatings():
    '''
    возвращает рейтинги, которые актуальны в данный момент, все остальные рейтинги не отображаются в общем списке
    '''
    today = date.today()
    #ratings = Rating.objects.filter(begin_date<=today, end_date>=today) #@UndefinedVariable
    ratings =  Rating.objects.filter(moderated=True)
    return ratings

def listArchievedRatings():
    '''
    возвращает архивные рейтинги, дата окончания которых находится в прошлом
    '''
    today = date.today()
    ratings = Rating.objects.filter(end_date<today) #@UndefinedVariable
    ratings =  Rating.objects.filter(moderated=True)
    return ratings
    
    