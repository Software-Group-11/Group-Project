from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, pattern):
    try:
        if context['sport'].name == pattern:
            return 'active'
    except:
        pass
    return ''
    