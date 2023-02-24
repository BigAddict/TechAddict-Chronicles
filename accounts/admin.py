from django.contrib import admin
from django.contrib.auth import get_user_model

from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import Bookmark, Profile

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "first_name", "last_name", "is_superuser"]
    search_fields = ["email", "first_name", "last_name"]

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "modified_at"]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "title"]
