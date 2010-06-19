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