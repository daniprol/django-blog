from ast import List

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .models import Post


def post_list(request: HttpRequest):
    post_list = Post.published.all()

    paginator = Paginator(post_list, 3)  # 3 posts per page
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
        # "posts" is an object of type Page
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/post/list.html", {"posts": posts})


class PostListView(ListView):
    """Alternative to post_list"""

    queryset = Post.published.all()
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
    return render(request, "blog/post/detail.html", {"post": post})
