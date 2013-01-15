from django import template
register = template.Library()


@register.inclusion_tag('social/like.html')
def like():
    return { }



@register.inclusion_tag('social/load.html')
def o2w_social():
    return {}
