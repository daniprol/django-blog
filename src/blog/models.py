from django.conf import settings
from django.db import models
from django.db.models.functions import Now
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)  # notice "Status" because it's the enum!

    def not_published(self):
        """Use with Post.published.not_published()"""
        return super().get_queryset().exclude(status=Post.Status.DRAFT)


# IMPORTANT: an index will be created on "author_id", "slug" and also "publish" columns!
class Post(models.Model):
    # FIRST DECLARED MANAGER WILL BE THE DEFAULT ONE!
    objects = models.Manager()  # DEFAULT MANAGER NEEDS TO BE DECLARED IF WE HAVE MORE!
    published = PublishedManager()  # INSTANTIATE THE MANAGER

    class Status(models.TextChoices):
        # (Values, Labels or readable names)
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"
        # NOTE: use Post.Status.values, Post.Status.labels, Post.Status.names

    title = models.CharField(max_length=250)  # VARCHAR
    # VARCHAR with only letters, numbers, hyphens and underscores
    slug = models.SlugField(max_length=250, unique_for_date="publish")  # will create INDEX by default
    # slug must be unique for each "publish" DATE (only date?) to be able to build a url like /yyyy/mm/dd/slug
    # NOTE: this is enforced in django, not in the DB. But migration will copy all table data to enforce uniqueness
    # Can also use primary-key=True for this one

    # add null=True (and blank=True ???) to allow anonymous users to create snippets as well
    # NOTE: if you want to create the foreign key on a field that is not a PK: to_field="email" or to_field=User.email
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts")
    # related_name: User object will have access to "blog_posts"
    # NOTICE THAT ADDING "author" WILL CREATE A "author_id" COLUMN!

    # NOTE: index will be created on author_id because using a ForeignKey implies creating an index by default!

    body = models.TextField()  # TEXT
    publish = models.DateTimeField(default=timezone.now)  # DATETIME
    # ALTERNATIVE:
    # publish = models.DateTimeField(db_default=Now()) # DB server CURRENT_TIMESTAMP
    created = models.DateTimeField(auto_now_add=True)  # DATETIME
    updated = models.DateTimeField(auto_now=True)  # DATETIME
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)

    tags = TaggableManager()
    # TAGS TABLE: id (pk), name, slug
    # TAGGEDITEM TABLE: id, tag (fk), content_type (fk), object_id (int)
    # (content_type, object_id) form a generic relationship between Tag and any other model instance of the app
    # To add tags: post.tags.add("ML", "LLM")
    # post.tags.remove("AI")

    class Meta:
        ordering = ["-publish"]  # latest posts first
        # NOTE: order applies by default to QuerySet unless an explicit order_by() is used
        indexes = [models.Index(fields=["-publish"])]
        # db_table = "custom_table_name"
        # Specify which manager will be the default one (for objects, django admin, serialization...)
        # default_manager_name = "published"

    def __str__(self):
        return self.title  # for Django-admin

    def get_absolute_url(self):
        # This will build the URL dynamically using the urlpatterns
        # return reverse("blog:post_detail", args=[self.id])
        return reverse("blog:post_detail", args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")  # plural because one-to-many
    # Notice that "post" will create "post_id" column instead!
    # Using related_name will allow you to post.comments.all().
    # By default it would be: post.comment_set

    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)  # useful for censorship

    class Meta:
        ordering = ["created"]  # oldest first?
        indexes = [
            models.Index(fields=["created"]),
        ]  # post_id index is automatically created!

    def __str__(self):
        return f"Comment by {self.name} on post {self.post}"  # self.post uses __str__ !
