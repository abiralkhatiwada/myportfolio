from django.contrib import admin
from django import forms

from django.conf import settings
from .models import Profile, Skill, Project, BlogPost, SocialLink, FlutterApp
import os
from django.contrib import admin


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "email")
    inlines = [SocialLinkInline]

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

class FlutterAppAdminForm(forms.ModelForm):
    class Meta:
        model = FlutterApp
        fields = '__all__'
        widgets = {
            # This field will be replaced by Cloudinary's upload widget
        }

@admin.register(FlutterApp)
class FlutterAppAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "order", "created_at", "updated_at")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "description", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_published", "order")
    ordering = ("order", "-created_at")

    class Media:
        # Load Cloudinary's upload widget JS
        js = ('https://upload-widget.cloudinary.com/global/all.js',)

    def changeform_view(self, request, *args, **kwargs):
        extra = {'cloudinary_cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME', '')}
        kwargs.setdefault('extra_context', {}).update(extra)
        return super().changeform_view(request, *args, **kwargs)
