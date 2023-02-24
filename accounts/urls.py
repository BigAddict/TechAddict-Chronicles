from django.urls import path

from .views import BookmarkView, SavedPostView, DraftPostView

app_name = "accounts"

urlpatterns = [
    path("bookmark/", BookmarkView.as_view(), name="bookmark"),
    path("<str:username>/saved/", SavedPostView.as_view(), name="saved_post"),
    path("<str:username>/draft/", DraftPostView.as_view(), name="draft_post"),
]
