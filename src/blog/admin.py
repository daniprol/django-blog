from django.contrib import admin

from .models import Post

# admin.site.register(Post)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    # Allows to search for user name when creating a post, instead of having a dropdown
    raw_id_fields = ["author"]
    date_hierarchy = "publish"  # navigation on top of the table
    ordering = ["status", "publish"]

    # Will always show "counts". Instead of being toggable
    show_facets = admin.ShowFacets.ALWAYS
