from django import template
from home.models import Contact

register = template.Library()

# Contact snippets
@register.inclusion_tag('home/tags/contact.html', takes_context=True)
def contact(context):
    return {
        'contacts': Contact.objects.filter(showSnippet=True),
        'request': context['request'],
    }
