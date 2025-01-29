import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy

from .models import Post


class LatestPostsFeed(Feed):
    # <title>, <link> and <description> from feed
    title = "My blog"
    link = reverse_lazy("blog:post_list")  # URL won't be evaluated until project URL config is loaded
    description = "Latest posts of my blog"

    def items(self):
        # FIXME: does it work without all()??
        return Post.published.all()[:5]

    def item_title(self, obj):
        return obj.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish
