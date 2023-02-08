from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView

from .models import Post, Category


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to=reverse("blog:post_list"))

        # popular posts and categories on landing page
        featured_posts = Post.objects.all()[:10]

        popular_categories = Category.objects.all()[:6]
        return render(
            request,
            template_name="blog/landing_page.html",
            context={
                "featured_posts": featured_posts,
                "popular_categories": popular_categories,
            },
        )


class PostListView(ListView):
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return (
            Post.objects.select_related("category")
            .select_related("author")
            .filter(status=1)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_categories"] = Category.objects.all()[:6]

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Display post creation form and handle the process."""

    model = Post
    fields = ["category", "title", "content", "status"]
    template_name = "blog/post_create.html"

    def form_valid(self, form):
        # assign the current logged in user as author of the post
        form.instance.author = self.request.user
        if form.instance.status == 0:
            msg = "Your post has been saved as draft."
        elif form.instance.status == 1:
            msg = "Your post has been published."

        messages.success(self.request, msg)
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post_detail.html"
