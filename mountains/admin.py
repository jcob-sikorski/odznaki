from django.contrib import admin
from .models import Mountain, Photo, Badge

@admin.register(Mountain)
class MountainAdmin(admin.ModelAdmin):
    list_display = ('name', 'altitude', 'latitude', 'longitude')

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    filter_horizontal = ('mountains',) # Easier UI to select multiple mountains

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'matched_mountain', 'latitude', 'uploaded_at')