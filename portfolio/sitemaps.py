from django.contrib import sitemaps
from django.urls import reverse
from .models import BlogPost

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['portfolio:home', 'portfolio:blog_list']

    def location(self, item):
        return reverse(item)

class BlogSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
