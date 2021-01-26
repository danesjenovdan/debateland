from django import template
from home.models import Newsletter

register = template.Library()

# Newsletter snippet
@register.inclusion_tag('home/tags/newsletter.html', takes_context=True)
def newsletter(context):
    return {
        'newsletters': Newsletter.objects.filter(showSnippet=True),
        'request': context['request'],
    }
