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
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text="SEO Meta Description (optional, optimal length: 150-160 characters). If blank, excerpt is used."
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


# ---------------------------------------------------------------------------
# Contact, Education, and Experience models (merged into portfolio app)
# ---------------------------------------------------------------------------

class ContactInfo(models.Model):
    """Contact information linked to the singleton Profile."""
    profile = models.OneToOneField('portfolio.Profile', on_delete=models.CASCADE, related_name='contact')
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return f"Contact for {self.profile.name}"


class Education(models.Model):
    """Educational entry for the portfolio."""
    profile = models.ForeignKey('portfolio.Profile', on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)  # null = present
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower = first)")

    class Meta:
        ordering = ["order", "-start_date"]
        verbose_name = "Education"
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.institution} – {self.degree}"


class Experience(models.Model):
    """Work experience entry for the portfolio."""
    profile = models.ForeignKey('portfolio.Profile', on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)  # null = present
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower = first)")

    class Meta:
        ordering = ["order", "-start_date"]
        verbose_name = "Experience"
        verbose_name_plural = "Experience"

    def __str__(self):
        return f"{self.company} – {self.role}"
