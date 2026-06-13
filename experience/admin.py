from django.contrib import admin
from .models import Experience

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('company', 'role', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('company', 'role')
