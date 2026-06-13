from django.contrib import admin
from .models import Education

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("institution", "degree", "start_date", "end_date", "order")
    list_editable = ("order",)
    ordering = ("order", "-start_date")
    search_fields = ("institution", "degree", "field_of_study")
