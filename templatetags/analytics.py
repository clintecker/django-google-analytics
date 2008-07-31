from django import template
from django.db import models
from django.contrib.sites.models import Site

from django.template import Context, loader


register = template.Library()
Analytics = models.get_model('googleanalytics', 'analytics')

def do_get_analytics(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, code = token.split_contents()
    except ValueError:
        code = None
   
    if not code:
        current_site = Site.objects.get_current()
    else:
        if not (code[0] == code[-1] and code[0] in ('"', "'")):
            raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
        code = code[1:-1]
        current_site = None
    return AnalyticsNode(current_site, code)
    
class AnalyticsNode(template.Node):
    def __init__(self, site=None, code=None):
        self.site = site
        self.code = code
        
    def render(self, context):
        content = ''
        if self.site:
            code_set = self.site.analytics_set.all()
            if code_set:
                code = code_set[0].analytics_code
            else:
                return ''
        elif self.code:
            code = self.code
        else:
            return ''
        
        if code.strip() != '':
            t = loader.get_template('google_analytics/analytics_template.html')
            c = Context({
                'analytics_code': code,
            })
            return t.render(c)
        else:
            return ''
        
register.tag('analytics', do_get_analytics)
