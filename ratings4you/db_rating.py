# -*- coding: utf8 -*-
'''
Created on 26.06.2010

@author: alarin
'''
from datetime import date
from models import Rating

def listActualRatings():
    '''
    возвращает рейтинги, которые актуальны в данный момент, все остальные рейтинги не отображаются в общем списке
    '''
    today = date.today()
    ratings = Rating.objects.filter(begin_date<=today, end_date>=today) #@UndefinedVariable
    return ratings

def listArchievedRatings():
    '''
    возвращает архивные рейтинги, дата окончания которых находится в прошлом
    '''
    today = date.today()
    ratings = Rating.objects.filter(end_date<today) #@UndefinedVariable
    return ratings