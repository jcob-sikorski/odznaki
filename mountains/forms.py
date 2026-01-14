# mountains/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Photo, Mountain
from .utils import get_exif_data, check_proximity

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        # User only provides the file; location data is extracted automatically
        fields = ['image']

    def clean_image(self):
        """
        Validates the uploaded image file.
        Logic: 
        1. Extract GPS data from EXIF.
        2. Check if coordinates match a known mountain.
        3. Store these derived values to be used in the save() method.
        """
        image = self.cleaned_data.get('image')
        
        # 1. Attempt to extract EXIF data (Latitude/Longitude)
        lat, lon = get_exif_data(image)
        
        if not lat or not lon:
            raise ValidationError("This photo lacks GPS (EXIF) data. Please ensure location services were enabled on your camera.")

        # 2. Check proximity against all mountains in the database
        all_mountains = Mountain.objects.all()
        found_mountain = check_proximity(lat, lon, all_mountains)

        if not found_mountain:
            raise ValidationError(f"No match found! Your location ({lat:.4f}, {lon:.4f}) does not match any mountain peak in our database.")

        # 3. Store the found data temporarily on the form instance.
        # We cannot assign them to the database object yet because save() hasn't been called.
        # We attach 'cleaned_geo_data' to 'self' to pass it to the save() method below.
        self.cleaned_geo_data = {
            'latitude': lat,
            'longitude': lon,
            'matched_mountain': found_mountain
        }

        return image

    def save(self, commit=True):
        """
        Overridden save method.
        Injects the calculated GPS data and matched mountain (from clean_image)
        into the model instance before writing to the database.
        """
        instance = super().save(commit=False)
        
        # Retrieve the data we calculated during validation
        geo_data = getattr(self, 'cleaned_geo_data', None)
        if geo_data:
            instance.latitude = geo_data['latitude']
            instance.longitude = geo_data['longitude']
            instance.matched_mountain = geo_data['matched_mountain']
        
        if commit:
            instance.save()
        return instance