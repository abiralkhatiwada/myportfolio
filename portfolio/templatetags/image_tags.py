"""
image_tags.py — Custom template filters for image URL optimization.

Applies Cloudinary URL transformation parameters to auto-serve
correctly-sized, modern-format (WebP/AVIF) images, dramatically
reducing payload for mobile visitors.

Usage in templates:
    {% load image_tags %}
    {{ profile.profile_image.url|cloudinary_transform:"c_fill,w_480,h_480,f_auto,q_auto" }}
    {{ project.image.url|cloudinary_transform:"c_fill,w_600,h_180,f_auto,q_auto" }}

Gracefully degrades: if the URL is not a Cloudinary URL (e.g. local
dev without Cloudinary), the original URL is returned unchanged.
"""

import re
from django import template

register = template.Library()


CLOUDINARY_UPLOAD_PATTERN = re.compile(
    r"(https://res\.cloudinary\.com/[^/]+/image/upload/)(/v\d+/.+|v\d+/.+|.+)",
    re.IGNORECASE,
)


@register.filter(name="cloudinary_transform")
def cloudinary_transform(url, transformation):
    """
    Inject Cloudinary transformation parameters into an upload URL.

    Example:
        Input:  https://res.cloudinary.com/demo/image/upload/v1234/profile/photo.jpg
        Params: c_fill,w_480,h_480,f_auto,q_auto
        Output: https://res.cloudinary.com/demo/image/upload/c_fill,w_480,h_480,f_auto,q_auto/v1234/profile/photo.jpg
    """
    if not url:
        return url

    url = str(url)

    # Only transform genuine Cloudinary upload URLs
    match = CLOUDINARY_UPLOAD_PATTERN.match(url)
    if not match:
        # Local or other CDN URL — return as-is
        return url

    base = match.group(1)   # e.g. https://res.cloudinary.com/demo/image/upload/
    rest = match.group(2)   # e.g. v1234/profile/photo.jpg

    # Avoid double-injecting transformations
    if transformation in url:
        return url

    return f"{base}{transformation}/{rest}"


@register.filter(name="cloudinary_thumb")
def cloudinary_thumb(url, size="400"):
    """
    Shortcut: generate a square thumbnail at <size>px.
    """
    params = f"c_fill,w_{size},h_{size},f_auto,q_auto"
    return cloudinary_transform(url, params)
