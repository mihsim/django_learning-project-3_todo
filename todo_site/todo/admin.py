from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    """Adds read only field to admin interface."""
    readonly_fields = ('created_time',)


admin.site.register(Todo, TodoAdmin)
