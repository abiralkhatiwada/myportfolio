from django import template
from django.utils.safestring import mark_safe
import markdown as md

register = template.Library()

@register.filter(name='markdown')
def markdown_filter(text):
    """Converts a markdown string to HTML."""
    if not text:
        return ""
    # We include extensions for common formats like tables, fenced code blocks, and lists
    return mark_safe(md.markdown(text, extensions=[
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        'markdown.extensions.sane_lists',
        'markdown.extensions.nl2br'  # Converts newlines to breaks like linebreaks filter
    ]))
