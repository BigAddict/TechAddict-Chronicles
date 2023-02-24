from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View, ListView

from .models import Bookmark
from blog.models import Post


User = get_user_model()


class BookmarkView(View):
    """Handle bookmarking post using ajax calls."""

    def post(self, request):
        user = self.request.user
        post_id = request.POST.get("post_id")

        if not user.is_authenticated:
            messages.warning(self.request, "Login to your account to bookmark posts.")
            return JsonResponse({"is_bookmarked": False}, status=401)

        selected_post = Post.objects.get(pk=post_id)
        is_bookmarked = False  # initial assumption
        bookmark = Bookmark.objects.filter(user=user, post=selected_post).first()
        if bookmark:
            bookmark.delete()  # was already saved, unsave now
        else:
            Bookmark.objects.create(user=user, post=selected_post)
            is_bookmarked = True

        return JsonResponse(
            {"is_bookmarked": is_bookmarked, "post_id": post_id}, status=200
        )


class SavedPostView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Show list of bookmarked posts."""

    template_name = "user/saved_post.html"
    context_object_name = "bookmarks"
    paginate_by = 10

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

    def test_func(self):
        self.user = get_object_or_404(User, username=self.kwargs.get("username"))
        return self.request.user == self.user


class DraftPostView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "user/draft_post.html"
    context_object_name = "draft_posts"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user, status=0)

    def test_func(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return self.request.user == user
