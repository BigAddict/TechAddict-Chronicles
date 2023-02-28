from django.urls import path

from .views import (
    BookmarkView,
    DraftPostView,
    FollowView,
    LikeView,
    ProfileView,
    SavedPostView,
    UpdateProfileView,
)

app_name = "accounts"

urlpatterns = [
    path("bookmark/", BookmarkView.as_view(), name="bookmark"),
    path("follow/", FollowView.as_view(), name="follow"),
    path("like/", LikeView.as_view(), name="like"),
    path("<str:username>/", ProfileView.as_view(), name="profile"),
    path("<str:username>/update/", UpdateProfileView.as_view(), name="profile_update"),
    path("<str:username>/saved/", SavedPostView.as_view(), name="saved_post"),
    path("<str:username>/draft/", DraftPostView.as_view(), name="draft_post"),
]
