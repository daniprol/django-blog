from datetime import UTC

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from faker import Faker

from blog.models import Comment, Post


class Command(BaseCommand):
    help = "Add fake blog posts to database"

    def add_arguments(self, parser):
        parser.add_argument("num_posts", type=int, help="Number of blog posts to create.", default=10)
        parser.add_argument("--comments", "-c", type=int, help="Number of comments per post to create.", default=10)

    def handle(self, *args, **options):
        MAX_POSTS = 100000
        MAX_COMMENTS = 100
        num_posts = min(options["num_posts"], MAX_POSTS)
        num_comments = min(options["comments"], MAX_COMMENTS)
        verbosity = options.get("verbosity", 1)
        if num_posts < 1:
            self.stdout.write(self.style.ERROR("Number of posts must be greater or equal to 1"))
            return
        if num_comments < 0:
            self.stdout.write(self.style.ERROR("Number of comments must be greater or equal to 0"))
            return

        fake = Faker()
        User = get_user_model()

        if not User.objects.exists():
            self.stdout.write(self.style.ERROR("At least 1 existing user is required to generate posts"))
            return

        posts = []
        comments = []

        users = list(User.objects.all())

        for _ in range(num_posts):
            user = fake.random_element(users)
            post = Post(
                title=fake.sentence(nb_words=7),
                slug=fake.slug(),
                author=user,
                body=fake.paragraph(nb_sentences=10),
                publish=fake.date_time(tzinfo=UTC),
                status=fake.random_element(elements=list(Post.Status)),
            )
            posts.append(post)

        with connection.cursor() as cursor:
            cursor.execute("PRAGMA journal_mode=WAL;")
            # cursor.execute("PRAGMA journal_mode=MEMORY;")
            cursor.execute("PRAGMA synchronous=OFF;")
            cursor.execute("PRAGMA cache_size=10000;")  # default: 2000 pages
            # cursor.execute('PRAGMA page_size=4096;')  # default: 1024 bytes (1 KB), units: bytes

        with transaction.atomic():
            Post.objects.bulk_create(posts)

            for post in posts:
                for _ in range(num_comments):
                    comment = Comment(
                        post=post,
                        name=fake.name(),
                        email=fake.email(),
                        body=fake.paragraph(nb_sentences=5),
                        active=fake.boolean(chance_of_getting_true=95),
                    )
                    comments.append(comment)

            Comment.objects.bulk_create(comments)

        if verbosity > 1:
            for post in posts:
                self.stdout.write(self.style.SUCCESS(f"Generated post {post.slug}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully generated {num_posts} posts with {num_comments} comments."))
