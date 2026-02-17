from django.shortcuts import render, get_object_or_404
from .models import Profile, Skill, Project, BlogPost


def home(request):
    """Render the portfolio homepage with all sections."""
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    projects = Project.objects.all()
    recent_posts = BlogPost.objects.filter(is_published=True)[:3]

    context = {
        "profile": profile,
        "skills": skills,
        "projects": projects,
        "recent_posts": recent_posts,
    }
    return render(request, "pages/home.html", context)


def blog_list(request):
    """List all published blog posts."""
    profile = Profile.objects.first()
    posts = BlogPost.objects.filter(is_published=True)

    context = {
        "profile": profile,
        "posts": posts,
    }
    return render(request, "pages/blog_list.html", context)


def blog_detail(request, slug):
    """Display a single blog post."""
    profile = Profile.objects.first()
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)

    context = {
        "profile": profile,
        "post": post,
    }
    return render(request, "pages/blog_detail.html", context)
