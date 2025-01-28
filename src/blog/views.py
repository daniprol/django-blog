from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.http import Http404
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm
from .models import Post


def post_list(request: HttpRequest, tag_slug=None):
    post_list = Post.published.all()
    tag = None

    if tag_slug:  # path parameter only passed in "tag/<slug>"
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Start from the existing Post Queryset
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 3)  # 3 posts per page
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
        # "posts" is an object of type Page
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/post/list.html", {"posts": posts, "tag": tag})


class PostListView(ListView):
    """Alternative to post_list"""

    queryset = Post.published.all()
    # queryset = Post.published.all().prefetch_related('tags')
    # NOTE: using queryset = Post <===> queryset = Post.objects.all()
    context_object_name = "posts"  # how to pass the result of queryset to template context
    paginate_by = 3
    # Page is passed to context as "page_obj"
    template_name = "blog/post/list.html"  # default: "blog/post_list.html"

    # NOTE: 404 will be returned if trying to access a nonexisting pagination page


# def post_detail(request: HttpRequest, id: int):
def post_detail(request: HttpRequest, year: int, month: int, day: int, slug: str):
    # try:
    #     # Only look among published posts
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404(f"Post ID {id} not found")
    # ALTERNATIVE: cant use the manager though
    # post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    post = get_object_or_404(
        Post, status=Post.Status.PUBLISHED, slug=slug, publish__year=year, publish__month=month, publish__day=day
    )

    # Show only active comments
    comments = post.comments.filter(active=True)  # Notice that we return a Queryset!
    form = CommentForm()

    # List of similar posts by using tags
    # values_lists returns a list of tuples of the specified columns.
    # Flat makes it a single list if only 1 column is retrieved
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)

    N_SIMILAR_POSTS = 4
    # "annotate" is used to add new fields to the objects (usually functions)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by("-same_tags", "-publish")[:N_SIMILAR_POSTS]
    # TODO: check taggit's builtin post.tags.similar_objects() function
    return render(
        request,
        "blog/post/detail.html",
        {"post": post, "comments": comments, "form": form, "similar_posts": similar_posts},
    )


def post_share(request: HttpRequest, post_id: int):
    # Make sure to filter by published posts
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    # Used to show success message in the template when email is sent
    sent = False

    if request.method == "POST":
        # Use POST data to fill the form
        form = EmailPostForm(request.POST)
        # DO I NEED TO VALIDATE THE FORM TO GET form.clean_data?
        if form.is_valid():
            # ...
            data = form.cleaned_data
            # dict with fields and values: values are also NORMALIZED
            # If your form data does not validate, cleaned_data will contain only the valid fields.
            # TODO: check what happens in cleaned_data when only some fields are valid
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{data['name']} ({data['email']} recommends you read {post.title})"
            message = f"Read {post.title} at {post_url}\n\n{data['name']}'s comments: {data['comments']}"
            # from_email=None will make it use settings.DEFAULT_FROM_EMAIL
            send_mail(
                subject=subject, message=message, from_email=None, recipient_list=[data["to"]], fail_silently=False
            )
            sent = True
        # Else: form will be returns to template with: form.errors
    else:
        form = EmailPostForm()  # creates empty form
    return render(request, "blog/post/share.html", {"post": post, "form": form, "sent": sent})


# Only form submissions are allowed in this view. Otherwise a 405 status code will be returned
@require_POST
def post_comment(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    form = CommentForm(data=request.POST)

    if form.is_valid():
        # create a comment model instance but don't save it to the DB yet
        comment = form.save(commit=False)

        # assign it to the post
        comment.post = post
        comment.save()

    # If form is invalid will render the template with the form errors
    return render(request, "blog/post/comment.html", {"post": post, "form": form, "comment": comment})
