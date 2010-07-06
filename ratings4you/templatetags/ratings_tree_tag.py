# -*- coding: utf8 -*-
'''
@since: 04.06.2010
@author: alarin
'''

from django import template
from django.template import Context
from ratings4you.db_rating import listActualRatings

register = template.Library()

class RatingsTreeTagNode(template.Node):
    '''
    Дерево каталога рейтингов в левом столбце сайта.
    '''
    def render(self, context):
        #raise template.TemplateSyntaxError, context
        request = context['request']
        ratings = listActualRatings()
        t = template.loader.get_template('ratings/templatetags/ratings_tree_tag.html')
        return t.render(Context({'ratings': ratings}))


@register.tag(name="rating_catalog_tree")
def do_rating_catalog_tree_tag(parser, token):
    #raise template.TemplateSyntaxError, parser
    try:
        # split_contents() knows not to split quoted strings.
        tag_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r requires 0 argument" % token.contents.split()[0]
    return RatingsTreeTagNode()