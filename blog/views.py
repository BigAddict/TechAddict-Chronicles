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
        featured_posts = (
            Post.objects.select_related("category")
            .select_related("author")
            .filter(status=1)[:10]
        )
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


class PostCreateView(CreateView):
    pass


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post_detail.html"
