from datetime import UTC

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from blog.models import Post


class Command(BaseCommand):
    help = "Add fake blog posts to database"

    def add_arguments(self, parser):
        parser.add_argument("num_posts", type=int, help="Number of blog posts to create.", default=10)

    def handle(self, *args, **options):
        MAX_POSTS = 20
        num_posts = min(options["num_posts"], MAX_POSTS)
        if num_posts < 1:
            self.stdout.write(self.style.ERROR("Number of posts must be greater or equal to 1"))
            return

        fake = Faker()
        User = get_user_model()

        if not User.objects.exists():
            self.stdout.write(self.style.ERROR("At least 1 existing user is required to generate posts"))
            return

        for _ in range(num_posts):
            user = User.objects.order_by("?").first()
            post = Post.objects.create(
                title=fake.sentence(nb_words=7),
                slug=fake.slug(),
                author=user,
                body=fake.paragraph(nb_sentences=10),
                publish=fake.date_time(tzinfo=UTC),
                status=fake.random_element(elements=list(Post.Status)),
            )

            self.stdout.write(self.style.SUCCESS(f"Generated post {post.slug}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully generated {num_posts} posts."))
