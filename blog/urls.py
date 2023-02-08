from django.urls import path

from .views import HomePageView, PostListView, PostCreateView, PostDetailView

app_name = "blog"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("stories/", PostListView.as_view(), name="post_list"),
    path("p/new/", PostCreateView.as_view(), name="post_create"),
    path("p/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
]
