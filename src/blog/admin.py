from django.contrib import admin
from django.db.models import F
from unfold.admin import ModelAdmin

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(ModelAdmin):
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


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ["name", "email", "post", "created", "active"]
    list_filter = ["active", "created", "updated"]  # last day, last month...
    search_fields = ["name", "email", "body"]
    # You can define action as a normal function and add it here too
    actions = ["deactivate_comments", "toggle_activate"]

    def deactivate_comments(self, request, queryset):
        """Takes queryset of comments and deactivates them"""
        queryset.update(active=False)

    deactivate_comments.short_description = "Deactivate selected comments"

    def toggle_activate(self, request, queryset):
        # NOTE: "F" expressions allow to reference a model field to make operations without having to fetch them in Python first
        queryset.update(active=~F("active"))

    toggle_activate.short_description = "Toggle activate in selected comments"
