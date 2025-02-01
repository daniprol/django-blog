from django.contrib import admin
from django.db.models import F
from import_export.admin import ImportExportModelAdmin, ImportMixin
from import_export.formats.base_formats import CSV, XLSX

from blog.forms import CustomImportForm

from .models import Comment, Post
from .resources import PostResource

# admin.site.register(Post)


# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
@admin.register(Post)
class PostAdmin(ImportExportModelAdmin):
    resource_class = PostResource
    formats = [XLSX, CSV]
    # import_form_class = CustomImportForm

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

    def has_export_permission(self, request):
        return False


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
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
