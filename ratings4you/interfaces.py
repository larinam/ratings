#!/usr/bin/python
# -*- coding: utf8 -*-

'''
Created on 19.06.2010

@author: alarin
'''

class IModeratable:
    '''
    интерфейс, определяющий, что элемент подлежит модерации
    '''
    
    def isModerated(self):
        '''
        объект прошел модерацию и должен быть опубликован
        '''
        pass
    
    
class NameAsIdentifier:
    '''
    Абстрактный класс для каталогов, в которых каждый элемент имеет уникальное 
    имя и объект должен идентифицироваться по имени.
    '''
    name = "MyName"
    
    def __unicode__(self):
        return self.name