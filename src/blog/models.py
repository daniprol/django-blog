from django.conf import settings
from django.db import models
from django.db.models.functions import Now
from django.utils import timezone


# IMPORTANT: an index will be created on "author_id", "slug" and also "publish" columns!
class Post(models.Model):
    class Status(models.TextChoices):
        # (Values, Labels or readable names)
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"
        # NOTE: use Post.Status.values, Post.Status.labels, Post.Status.names

    title = models.CharField(max_length=250)  # VARCHAR
    # VARCHAR with only letters, numbers, hyphens and underscores
    slug = models.SlugField(max_length=250)  # will create INDEX by default
    # Can also use primary-key=True for this one

    # add null=True (and blank=True ???) to allow anonymous users to create snippets as well
    # NOTE: if you want to create the foreign key on a field that is not a PK: to_field="email" or to_field=User.email
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts")
    # related_name: User object will have access to "blog_posts"

    # NOTE: index will be created on author_id because using a ForeignKey implies creating an index by default!

    body = models.TextField()  # TEXT
    publish = models.DateTimeField(default=timezone.now)  # DATETIME
    # ALTERNATIVE:
    # publish = models.DateTimeField(db_default=Now()) # DB server CURRENT_TIMESTAMP
    created = models.DateTimeField(auto_now_add=True)  # DATETIME
    updated = models.DateTimeField(auto_now=True)  # DATETIME
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)

    class Meta:
        ordering = ["-publish"]  # latest posts first
        # NOTE: order applies by default to QuerySet unless an explicit order_by() is used
        indexes = [models.Index(fields=["-publish"])]
        # db_table = "custom_table_name"

    def __str__(self):
        return self.title  # for Django-admin
