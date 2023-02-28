from django.urls import path

from .views import (
    CategoryView,
    CommentView,
    HomePageView,
    PostListView,
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
)

app_name = "blog"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("stories/", PostListView.as_view(), name="post_list"),
    path("p/new/", PostCreateView.as_view(), name="post_create"),
    path("p/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("p/<slug:slug>/edit/", PostUpdateView.as_view(), name="post_update"),
    path("p/<slug:slug>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("p/<slug:slug>/comments/", CommentView.as_view(), name="comment"),
    path("category/<slug:slug>/", CategoryView.as_view(), name="category"),
]
