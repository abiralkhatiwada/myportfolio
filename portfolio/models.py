from django.db import models
from django.utils.text import slugify


class Profile(models.Model):
    """Singleton model for the site owner's profile."""
    name = models.CharField(max_length=100, default="Abiral Khatiwada")
    title = models.CharField(max_length=200, default="Flutter Developer | AI Enthusiast")
    bio = models.TextField(
        default="I'm a passionate Flutter developer and AI enthusiast who loves turning "
                "creative ideas into functional apps. My goal is to blend mobile development "
                "with artificial intelligence to deliver smarter user experiences."
    )
    tagline = models.CharField(
        max_length=300,
        default="Building intelligent, beautiful, and user-friendly apps that make life easier."
    )
    email = models.EmailField(default="abiralkhatiwada37@gmail.com")
    profile_image = models.ImageField(upload_to="profile/", blank=True, null=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Enforce singleton: only one Profile can exist
        if not self.pk and Profile.objects.exists():
            raise ValueError("Only one Profile instance is allowed.")
        super().save(*args, **kwargs)


class Skill(models.Model):
    """A skill to display in the Skills section."""

    CATEGORY_CHOICES = [
        ('core', 'Core'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('tools', 'Tools'),
        ('frontend', 'Frontend'),
        ('advanced', 'Advanced'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='core'  # IMPORTANT: prevents migration issues
    )
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower = first)")

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    """A project to showcase in the Projects section."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    link = models.URLField(blank=True)
    link_text = models.CharField(max_length=50, default="View Project →")
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower = first)")

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


from django.urls import reverse

class BlogPost(models.Model):
    """A blog post with slug-based URLs."""
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    excerpt = models.TextField(
        max_length=500,
        help_text="Short summary shown on the blog listing page."
    )
    content = models.TextField(help_text="Full blog post content.")
    image = models.ImageField(upload_to="blog/", blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:blog_detail", kwargs={"slug": self.slug})


class SocialLink(models.Model):
    """Dynamic social media links for the profile."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="social_links")
    platform = models.CharField(max_length=50, help_text="e.g. GitHub, LinkedIn, Twitter, Instagram, etc.")
    url = models.URLField()
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower = first)")

    class Meta:
        ordering = ["order", "platform"]

    def __str__(self):
        return f"{self.platform} - {self.profile.name}"
