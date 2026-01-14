# mountains/models.py
from django.db import models
from django.contrib.auth.models import User

class Mountain(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.IntegerField()
    # Radius in meters to determine if a user is "at" the peak
    radius = models.IntegerField(default=200)

    def __str__(self):
        return f"{self.name} ({self.altitude} m)"

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='badges/', blank=True, null=True) 
    
    # Many-to-Many: A badge requires a specific set of mountains.
    # 'related_name' allows us to access badges from a mountain instance (mountain.badges.all())
    mountains = models.ManyToManyField(Mountain, related_name='badges')

    def __str__(self):
        return self.name

class Photo(models.Model):
    # Links the photo to a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='peaks/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Stored separately to preserve location even if Mountain definitions change later
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # The system's best guess at which mountain this is. 
    # SET_NULL ensures photo remains even if the mountain is deleted from DB.
    matched_mountain = models.ForeignKey(Mountain, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Photo {self.user.username} - {self.matched_mountain}"