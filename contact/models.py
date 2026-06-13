from django.db import models


class ContactInfo(models.Model):
    """Model to store contact details linked to the Profile singleton."""
    profile = models.OneToOneField('portfolio.Profile', on_delete=models.CASCADE, related_name='contact')
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return f"Contact for {self.profile.name}"
