from django.shortcuts import render, get_object_or_404
from .models import Profile, Skill, Project, BlogPost, FlutterApp


from collections import defaultdict

def home(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    projects = Project.objects.all()
    recent_posts = BlogPost.objects.filter(is_published=True)[:3]

    grouped_skills = defaultdict(list)
    for skill in skills:
        grouped_skills[skill.category].append(skill)

    context = {
        "profile": profile,
        "grouped_skills": dict(grouped_skills),
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


def app_list(request):
    """List all published Flutter apps."""
    profile = Profile.objects.first()
    apps = FlutterApp.objects.filter(is_published=True)

    context = {
        "profile": profile,
        "apps": apps,
    }
    return render(request, "pages/app_list.html", context)


def app_detail(request, slug):
    """Display a single Flutter app."""
    profile = Profile.objects.first()
    app = get_object_or_404(FlutterApp, slug=slug, is_published=True)

    context = {
        "profile": profile,
        "app": app,
    }
    return render(request, "pages/app_detail.html", context)

from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings

def contact_submit(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        
        subject = f"New Portfolio Contact from {name}"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        
        try:
            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, "An error occurred. Please try again.")
            
    return redirect("portfolio:home")

