from django.urls import path

from . import views

# DEFINES AN APPLICATION NAMESPACE
app_name = "blog"
# Needed for namespace URL reversing (e.g. reverse("blog:post_detail"))
# If you only use "namespace" in the "include" function of the global urlpatterns you won't be able to reverse URL within this app
urlpatterns = [
    path("", views.post_list, name="post_list"),
    # path("", views.PostListView.as_view(), name="post_list"),
    path("tag/<slug:tag_slug>/", views.post_list, name="post_list_by_tag"),  # different name for the view
    # Can we use <int:pk> too?
    # path("<int:id>", views.post_detail, name="post_detail"),
    # This will be called as post_detail(request, id=<id>)
    path("<int:year>/<int:month>/<int:day>/<slug:slug>/", views.post_detail, name="post_detail"),
    path("<int:post_id>/share/", views.post_share, name="post_share"),
    path("<int:post_id>/comment/", views.post_comment, name="post_comment"),
]
