from typing import Any

from django import template
from django.conf import settings
from django.db.models import Count
from django.utils.safestring import mark_safe
from markdown import markdown

from ..models import Post

# Register custom templating tags {% custom %}
register = template.Library()


# SIMPLE TAG: receives data and outputs a str
@register.simple_tag  # use name="custom_name" to add another name
def total_posts():
    return Post.published.count()


# Simple template tag that returns a queryset that can be reused in multiple places:
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count("comments")).order_by("-total_comments")[:count]


# INCLUSION TAG: allow you to render a template with context variables
# They always must return a dictionary!
# No need to use {% load tagname %}
@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count: int = 5) -> dict[str, Any]:  # optional argument
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


@register.filter(name="markdown")
def markdown_format(text):
    # NOTE: by default Django scapes all generated HTML code output in filters, so we  need to mark it as safe
    return mark_safe(markdown(text))


@register.filter(name="get")
def get(o, index):
    try:
        return o[index]
    except Exception:
        return settings.TEMPLATE_STRING_IF_INVALID


@register.filter(name="getattr")
def getattrfilter(o, attr):
    try:
        attr = getattr(o, attr, None)
        return attr
    except Exception:
        return settings.TEMPLATE_STRING_IF_INVALID
