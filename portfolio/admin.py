from django.contrib import admin
from django.utils import timezone

from .models import BlogPost, FlutterApp, Profile, Project, Skill, SocialLink


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "email")
    inlines = [SocialLinkInline]

    def has_add_permission(self, request):
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
    list_display = (
        "title",
        "status",
        "is_published",
        "ai_generated",
        "scheduled_at",
        "created_at",
    )
    list_filter = (
        "status",
        "is_published",
        "ai_generated",
        "created_at",
    )
    search_fields = (
        "title",
        "content",
        "excerpt",
        "keywords",
    )
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = (
        "created_at",
        "updated_at",
        "reviewed_at",
    )
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Article Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "excerpt",
                    "content",
                    "image",
                )
            },
        ),
        (
            "SEO Settings",
            {
                "fields": (
                    "seo_title",
                    "meta_description",
                    "keywords",
                )
            },
        ),
        (
            "Publishing Workflow",
            {
                "fields": (
                    "status",
                    "is_published",
                    "scheduled_at",
                    "ai_generated",
                    "reviewed_at",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    actions = [
        "mark_pending_review",
        "approve_articles",
        "reject_articles",
        "publish_articles",
        "unpublish_articles",
    ]

    @admin.action(description="Move selected articles to Pending Review")
    def mark_pending_review(self, request, queryset):
        queryset.update(
            status="pending_review",
            is_published=False,
        )

    @admin.action(description="Approve selected articles")
    def approve_articles(self, request, queryset):
        queryset.update(
            status="approved",
            is_published=False,
            reviewed_at=timezone.now(),
        )

    @admin.action(description="Reject selected articles")
    def reject_articles(self, request, queryset):
        queryset.update(
            status="rejected",
            is_published=False,
        )

    @admin.action(description="Publish selected articles immediately")
    def publish_articles(self, request, queryset):
        queryset.update(
            status="published",
            is_published=True,
            scheduled_at=None,
            reviewed_at=timezone.now(),
        )

    @admin.action(description="Unpublish selected articles")
    def unpublish_articles(self, request, queryset):
        queryset.update(
            status="draft",
            is_published=False,
        )


@admin.register(FlutterApp)
class FlutterAppAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_published",
        "order",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "description", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_published", "order")
    ordering = ("order", "-created_at")