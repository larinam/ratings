# -*- coding: utf8 -*-
'''
@since: 04.06.2010
@author: alarin
'''

from django import template
from django.template import Context
from ratings4you.db_rating import listTopRatingItems

register = template.Library()

class TopRatingItemsTagNode(template.Node):
    '''
    Дерево каталога рейтингов в левом столбце сайта.
    '''
    def render(self, context):
        #raise template.TemplateSyntaxError, context
        request = context['request']
        rating_items = listTopRatingItems(20)
        t = template.loader.get_template('ratings/templatetags/top_rating_items_tag.html')
        return t.render(Context({'rating_items': rating_items}))


@register.tag(name="top_rating_items")
def do_top_rating_items_tag(parser, token):
    #raise template.TemplateSyntaxError, parser
    try:
        # split_contents() knows not to split quoted strings.
        tag_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r requires 0 argument" % token.contents.split()[0]
    return TopRatingItemsTagNode()