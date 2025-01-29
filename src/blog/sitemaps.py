from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSitemap(Sitemap):
    # Both change_freq and priority can be methods or atributes
    change_freq = "weekly"
    priority = 0.9  # relevance of the object in this site

    def items(self):
        # NOTE: by default Django will call get_absolute_url() to get the URL of each object
        # to specify another location for objects add a "location" method here
        return Post.published.order_by("-publish")[:100]

    def lastmod(self, obj):
        # Last modification of each object returned by items()
        return obj.updated
