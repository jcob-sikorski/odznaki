from django.db import models
from django.contrib.auth.models import User

class Mountain(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.IntegerField()
    radius = models.IntegerField(default=200)

    def __str__(self):
        return f"{self.name} ({self.altitude} m)"

# --- NEW CODE START ---
class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='badges/', blank=True, null=True) # Icon for the badge
    mountains = models.ManyToManyField(Mountain, related_name='badges')

    def __str__(self):
        return self.name
# --- NEW CODE END ---

class Photo(models.Model):
    # (Existing code remains the same)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='peaks/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    matched_mountain = models.ForeignKey(Mountain, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Zdjęcie {self.user.username} - {self.matched_mountain}"