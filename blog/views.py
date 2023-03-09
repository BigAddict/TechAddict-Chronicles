from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import CommentForm
from .models import Post, Category, Comment


def get_saved_posts(user):
    """Return list of saved posts by the user (if any)"""
    if not user.is_authenticated:
        return []
    return [b.post for b in user.bookmark_set.all()]


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to=reverse("blog:post_list"))

        return render(
            request,
            "blog/landing_page.html",
            context={
                "featured_posts": Post.objects.all()[:10],
                "popular_categories": Category.objects.all()[:6],
            },
        )


class PostListView(ListView):
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(status=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_categories"] = Category.objects.all()[:6]
        context["saved_posts"] = get_saved_posts(self.request.user)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Display post creation form and handle the process."""

    model = Post
    fields = ["category", "title", "content", "status"]
    template_name = "blog/post_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        msg = "Your post has been published."
        if form.instance.status == 0:
            msg = "Your post has been saved as draft."

        messages.success(self.request, msg)
        return super().form_valid(form)


class PostDetailView(UserPassesTestMixin, DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 3 related/popular posts to the current post
        current_post_slug = self.kwargs.get("slug")
        related_posts = Post.objects.all().exclude(slug=current_post_slug)[:3]
        context["related_posts"] = related_posts
        context["saved_posts"] = get_saved_posts(self.request.user)
        return context

    def test_func(self):
        if self.get_object().status == 0:
            # drafts can be seen by their author only
            return self.get_object().author == self.request.user
        return True


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Display post update form and handle the process."""

    model = Post
    fields = ["category", "title", "content", "status"]
    template_name = "blog/post_update.html"

    def test_func(self):
        return self.get_object().author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Display post deletion form and handle the process."""

    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("blog:post_list")

    def test_func(self):
        return self.get_object().author == self.request.user


class CategoryView(ListView):
    """Show all post in a category."""

    model = Category
    template_name = "blog/category.html"
    context_object_name = "category_posts"
    paginate_by = 10

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs["slug"])
        return category.post_set.all().filter(status=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.get(slug=self.kwargs["slug"])
        context["popular_categories"] = Category.objects.all()[:6]
        context["saved_posts"] = get_saved_posts(self.request.user)
        return context


class SearchResultView(ListView):
    model = Post
    context_object_name = "search_results"
    template_name = "blog/search_result.html"
    paginate_by = 10

    def get_queryset(self):
        self.user_input = self.request.GET.get("q", "")
        query = SearchQuery(self.user_input)
        vector = SearchVector(
            "title", "content", "category__name", "author__first_name"
        )
        search_results = Post.objects.annotate(
            search=vector, rank=SearchRank(vector, query)
        )
        search_results = search_results.filter(search=query).order_by("-rank")
        return search_results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        context["query"] = self.user_input
        context["total"] = len(queryset)
        context["saved_posts"] = get_saved_posts(self.request.user)
        return context


class CommentView(View):
    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(post__slug=kwargs.get("slug"))
        selected_post = get_object_or_404(Post, slug=kwargs.get("slug"))
        context = {
            "comment_form": CommentForm(),
            "comments": comments,
            "post": selected_post,
        }
        return render(request, "blog/comment.html", context)

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return messages.warning(
                request, "Login to your account to comment on posts."
            )

        selected_post = get_object_or_404(Post, slug=kwargs.get("slug"))
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.author = request.user
            comment_form.instance.post = selected_post
            comment_form.save()
            messages.info(request, "Your comment has been published.")

        comments = Comment.objects.filter(post__slug=kwargs.get("slug"))
        context = {
            "comment_form": CommentForm(),
            "comments": comments,
            "post": selected_post,
        }
        return render(request, "blog/comment.html", context)
