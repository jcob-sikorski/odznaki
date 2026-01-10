# mountains/admin.py
from django.contrib import admin
from .models import Mountain, Photo

@admin.register(Mountain)
class MountainAdmin(admin.ModelAdmin):
    list_display = ('name', 'altitude', 'latitude', 'longitude')

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'matched_mountain', 'latitude', 'longitude', 'uploaded_at')
    readonly_fields = ('latitude', 'longitude', 'matched_mountain')