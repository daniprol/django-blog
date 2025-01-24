from django.http import Http404
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, render

from .models import Post


def post_list(request: HttpRequest):
    posts = Post.published.all()
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request: HttpRequest, id: int):
    # try:
    #     # Only look among published posts
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404(f"Post ID {id} not found")
    # ALTERNATIVE: cant use the manager though
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)

    return render(request, "blog/post/detail.html", {"post": post})
