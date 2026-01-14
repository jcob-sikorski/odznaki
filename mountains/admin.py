# mountains/admin.py
from django.contrib import admin
from .models import Mountain, Photo, Badge

@admin.register(Mountain)
class MountainAdmin(admin.ModelAdmin):
    # Columns displayed in the list view of Mountains
    list_display = ('name', 'altitude', 'latitude', 'longitude')

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    # Uses a specialized JavaScript widget for ManyToMany fields
    # This makes selecting multiple mountains for a badge much easier than a standard multi-select box
    filter_horizontal = ('mountains',) 

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    # Display the user, the auto-detected mountain, and upload timestamp
    list_display = ('user', 'matched_mountain', 'latitude', 'uploaded_at')