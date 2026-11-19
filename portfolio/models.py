from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Profile(models.Model):
    """Singleton model for the site owner's profile."""

    name = models.CharField(max_length=100, default="Abiral Khatiwada")
    title = models.CharField(
        max_length=200,
        default="Flutter Developer | AI Enthusiast",
    )
    bio = models.TextField(
        default=(
            "I'm a passionate Flutter developer and AI enthusiast who loves turning "
            "creative ideas into functional apps. My goal is to blend mobile development "
            "with artificial intelligence to deliver smarter user experiences."
        )
    )
    tagline = models.CharField(
        max_length=300,
        default="Building intelligent, beautiful, and user-friendly apps that make life easier.",
    )
    email = models.EmailField(default="abiralkhatiwada37@gmail.com")
    profile_image = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and Profile.objects.exists():
            raise ValueError("Only one Profile instance is allowed.")
        super().save(*args, **kwargs)


class Skill(models.Model):
    """A skill to display in the Skills section."""

    CATEGORY_CHOICES = [
        ("core", "Core"),
        ("backend", "Backend"),
        ("database", "Database"),
        ("tools", "Tools"),
        ("frontend", "Frontend"),
        ("advanced", "Advanced"),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="core",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower = first)",
    )

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    """A project to showcase in the Projects section."""

    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True,
    )
    link = models.URLField(blank=True)
    link_text = models.CharField(
        max_length=50,
        default="View Project →",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower = first)",
    )

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    """A blog post with SEO and publishing workflow."""

    STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('pending_review', 'Pending Review'),
    ('approved', 'Approved'),
    ('scheduled', 'Scheduled'),
    ('published', 'Published'),
    ('rejected', 'Rejected'),
]

    # Basic article information
    title = models.CharField(max_length=300)
    slug = models.SlugField(
        max_length=300,
        unique=True,
        blank=True,
    )
    excerpt = models.TextField(
        max_length=500,
        help_text="Short summary shown on the blog listing page.",
    )
    content = models.TextField(help_text="Full blog post content.")
    image = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True,
    )

    # SEO information
    seo_title = models.CharField(
        max_length=300,
        blank=True,
        help_text="SEO title. Leave blank to use the article title.",
    )
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text="SEO description (ideally 150-160 characters).",
    )
    keywords = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated article keywords.",
    )

    # Publishing workflow
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )
    is_published = models.BooleanField(default=False)
    scheduled_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Date and time when the article should be published.",
    )

    # Article generation and review
    ai_generated = models.BooleanField(
        default=False,
        help_text="Was this article generated with AI assistance?",
    )
    reviewed_at = models.DateTimeField(blank=True, null=True)

    # Timestamps
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

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="social_links",
    )
    platform = models.CharField(
        max_length=50,
        help_text="e.g. GitHub, LinkedIn, Twitter, Instagram, etc.",
    )
    url = models.URLField()
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower = first)",
    )

    class Meta:
        ordering = ["order", "platform"]

    def __str__(self):
        return f"{self.platform} - {self.profile.name}"


class FlutterApp(models.Model):
    """A Flutter application with downloadable APK."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
    )
    excerpt = models.TextField(
        max_length=500,
        help_text="Short summary shown on the app listing page.",
    )
    description = models.TextField(help_text="Detailed description of the app.")
    icon = models.ImageField(
        upload_to="apps/icons/",
        blank=True,
        null=True,
    )
    screenshot = models.ImageField(
        upload_to="apps/screenshots/",
        blank=True,
        null=True,
    )
    apk_file = models.URLField(
        help_text="Paste the direct GitHub Release download URL of the APK.",
        blank=True,
    )
    is_published = models.BooleanField(default=False)
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower = first)",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:app_detail", kwargs={"slug": self.slug})