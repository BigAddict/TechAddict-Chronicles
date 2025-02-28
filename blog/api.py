from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from .models import Post, Category

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token


User = get_user_model()

@api_view(['GET'])
def get_categories(request):
    """API to list all categories"""
    categories = Category.objects.values("id", "name")
    return Response({"categories": list(categories)})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_post(request):
    """API to create a blog post via n8n"""
    title = request.data.get('title')
    content = request.data.get('content')
    category_id = request.data.get('category_id')
    status = request.data.get('status', 0)  # Default is Draft

    if not title or not content:
        return Response({"error": "Title and content are required"}, status=400)

    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"error": "Invalid category ID"}, status=400)

    author = User.objects.first()  # Assign first user as default (modify as needed)
    slug = slugify(title)  # Generate unique slug

    post = Post.objects.create(
        title=title, content=content, slug=slug, author=author, category=category, status=status
    )

    return Response({"message": "Post created!", "post_id": post.id, "slug": post.slug}, status=201)

@api_view(['GET'])
def get_posts(request):
    """API to list all posts"""
    posts = Post.objects.values("id", "title", "slug", "status", "content", "category__name")
    return Response({"posts": list(posts)})