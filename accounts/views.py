from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import View, ListView

from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Bookmark
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
