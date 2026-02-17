from django.contrib import admin
from .models import Profile, Skill, Project, BlogPost


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "email")

    def has_add_permission(self, request):
        # Only allow adding if no Profile exists yet
        return not Profile.objects.exists()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "link")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at", "updated_at")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_published",)
    ordering = ("-created_at",)
