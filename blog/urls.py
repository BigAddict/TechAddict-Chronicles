from django.urls import path

from .views import (
    HomePageView,
    PostListView,
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    CategoryView,
)

app_name = "blog"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("stories/", PostListView.as_view(), name="post_list"),
    path("p/new/", PostCreateView.as_view(), name="post_create"),
    path("p/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("p/<slug:slug>/edit/", PostUpdateView.as_view(), name="post_update"),
    path("p/<slug:slug>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("category/<slug:slug>/", CategoryView.as_view(), name="category"),
]
