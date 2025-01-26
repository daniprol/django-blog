from django.urls import path

from . import views

# DEFINES AN APPLICATION NAMESPACE
app_name = "blog"

urlpatterns = [
    # path("", views.post_list, name="post_list"),
    path("", views.PostListView.as_view(), name="post_list"),
    # Can we use <int:pk> too?
    # path("<int:id>", views.post_detail, name="post_detail"),
    # This will be called as post_detail(request, id=<id>)
    path("<int:year>/<int:month>/<int:day>/<slug:slug>/", views.post_detail, name="post_detail"),
    path("<int:post_id>/share/", views.post_share, name="post_share"),
]
