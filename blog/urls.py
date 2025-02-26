from django.urls import path

from .views import (
    CategoryView,
    CreateCategoryView,
    CommentView,
    HomePageView,
    PostListView,
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    SearchResultView,
)
from .api import get_categories, create_post, get_posts

app_name = "blog"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("stories/", PostListView.as_view(), name="post_list"),
    path("search/", SearchResultView.as_view(), name="search"),
    path("p/new/", PostCreateView.as_view(), name="post_create"),
    path("p/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("p/<slug:slug>/edit/", PostUpdateView.as_view(), name="post_update"),
    path("p/<slug:slug>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("p/<slug:slug>/comments/", CommentView.as_view(), name="comment"),
    path("category/<slug:slug>/", CategoryView.as_view(), name="category"),
    path('api/categories/', get_categories, name='get-categories'),
    path("api/categories/create/", CreateCategoryView.as_view(), name="create-category"),
    path('api/create-post/', create_post, name='create-post'),
    path('api/posts/', get_posts, name='get-posts'),
]
