from django.urls import path
from blogging.views import PostListView, PostDetailView, add_post

urlpatterns = [
    path("", PostListView.as_view(), name="blog_index"),
    path("add/", add_post, name="add_post"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="blog_detail"),
]
