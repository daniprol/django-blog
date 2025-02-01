import logging

from django.contrib.auth.models import User
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from .models import Post

logger = logging.getLogger(__name__)


class PostResource(resources.ModelResource):
    author = fields.Field(
        column_name="author",
        attribute="author",
        # TODO: try with settings.AUTH_USER_MODEL and email
        widget=ForeignKeyWidget(User, "username"),
    )

    class Meta:
        model = Post
        fields = ("title", "author", "body", "publish", "status")
        import_id_fields = ("title",)
        skip_unchanged = True
        report_skipped = True
        use_bulk = False  # first row treated as header

    def before_import_row(self, row, row_number=None, **kwargs):
        if not row.get("status"):
            row["status"] = Post.Status.DRAFT.value  # DF

    def import_row(self, row, instance_loader, **kwargs):
        try:
            return super().import_row(row, instance_loader, **kwargs)
        except Exception as e:
            logger.error(f"Error importing row: {row}. Error: {e}")
            self.errors.append((row, str(e)))
            return False
