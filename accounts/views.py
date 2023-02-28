from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import View, ListView

from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Bookmark, Like, UserFollowing
from blog.models import Post


User = get_user_model()


class ProfileView(ListView):
    """Show user profile page"""

    context_object_name = "author_posts"
    template_name = "user/profile.html"
    paginate_by = 10

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=self.author, status=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = self.author
        return context


class UpdateProfileView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Show profile update form and handle the process."""

    def get(self, request, **kwargs):
        context = {
            "user_form": UserUpdateForm(instance=request.user),
            "profile_form": ProfileUpdateForm(instance=request.user.profile),
        }
        return render(request, "user/profile_update.html", context)

    def post(self, request, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect(
                to=reverse("accounts:profile", args=(self.request.user.username,))
            )

    def test_func(self):
        self.author = get_object_or_404(User, username=self.kwargs.get("username"))
        return self.request.user == self.author


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


class BookmarkView(View):
    """Handle bookmarking post using ajax calls."""

    def post(self, request):
        user = self.request.user
        post_id = request.POST.get("post_id")

        if not user.is_authenticated:
            messages.warning(self.request, "Login to your account to bookmark posts.")
            return JsonResponse({"is_saved": False}, status=401)

        selected_post = Post.objects.get(pk=post_id)
        bookmark, created = Bookmark.objects.get_or_create(
            user=user, post=selected_post
        )
        if created:
            is_saved = True  # saved now
        else:
            is_saved = False  # was already saved, unsave now
            bookmark.delete()

        return JsonResponse({"is_saved": is_saved, "post_id": post_id}, status=200)


class LikeView(View):
    """Handle like and unlike posts using ajax calls."""

    def post(self, request):
        user = self.request.user
        post_id = request.POST.get("post_id")

        if not user.is_authenticated:
            messages.info(self.request, "Login to your account to like posts.")
            return JsonResponse(data={"is_liked": False}, status=401)

        selected_post = Post.objects.get(pk=post_id)
        like, created = Like.objects.get_or_create(user=user, post=selected_post)
        if created:
            is_liked = True  # liked the post now
        else:
            is_liked = False  # was already liked, unlike now
            like.delete()

        data = {"is_liked": is_liked, "likes_count": selected_post.like_set.count()}
        return JsonResponse(data, status=200)


class FollowView(View):
    """Handle follow/unfollow activity."""

    def post(self, request, *args, **kwargs):
        current_user = self.request.user
        if not current_user.is_authenticated:
            messages.info(self.request, "Login to your account to follow others.")
            return JsonResponse({"is_authenticated": False}, status=401)

        # target user to follow or unfollow
        # TODO: what if target user not found or similar to current user?
        target_user = User.objects.get(pk=request.POST["user_id"])

        user_followed, created = UserFollowing.objects.get_or_create(
            user=current_user, user_following=target_user
        )
        if created:
            is_following = True  # started following now
        else:
            is_following = False
            user_followed.delete()  # was already following, unfollow now

        return JsonResponse({"is_following": is_following}, status=200)
