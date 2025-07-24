from django.contrib import admin

# Register your models here.

from .models import Project, TimeEntry

admin.site.register(Project)
admin.site.register(TimeEntry)
