# -*- coding: utf8 -*-
'''
@since: 04.06.2010
@author: alarin
'''

from django import template
from django.template import Context
from django.contrib.auth.models import User

register = template.Library()

class UserNameTagNode(template.Node):
    '''
    Превращает id пользователя в username пользователя. 
    '''
    
    def __init__(self, user_id=None):
        self.user_id = template.Variable(user_id)

    def render(self, context):
        #raise template.TemplateSyntaxError, context
        user_id = self.user_id.resolve(context)
        request = context['request']
        author = User.objects.get(pk=int(user_id))
        return author.username


@register.tag(name="user_id_to_name")
def do_user_id_to_name_tag(parser, token):
    #raise template.TemplateSyntaxError, parser
    try:
        # split_contents() knows not to split quoted strings.
        tag_name = token.split_contents()
        user_id = token.split_contents()[1]
    except ValueError:
        raise template.TemplateSyntaxError, "%r requires 1 argument" % token.contents.split()[0]
    return UserNameTagNode(user_id=user_id)