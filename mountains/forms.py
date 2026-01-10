# mountains/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Photo, Mountain
from .utils import get_exif_data, check_proximity

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

    def clean_image(self):
        """Walidacja samego pliku zdjęcia."""
        image = self.cleaned_data.get('image')
        
        # 1. Próba wyciągnięcia EXIF
        lat, lon = get_exif_data(image)
        
        if not lat or not lon:
            raise ValidationError("To zdjęcie nie posiada danych GPS (EXIF). Upewnij się, że masz włączoną lokalizację w aparacie.")

        # 2. Sprawdzenie czy jesteśmy blisko jakiejś góry
        all_mountains = Mountain.objects.all()
        found_mountain = check_proximity(lat, lon, all_mountains)

        if not found_mountain:
            raise ValidationError(f"Brak dopasowania! Twoja lokalizacja ({lat:.4f}, {lon:.4f}) nie pasuje do żadnego szczytu w bazie.")

        # 3. Zapisujemy znalezione dane w instancji formularza (żeby użyć ich przy zapisie)
        # Używamy atrybutu tymczasowego na 'self', żeby przekazać dane do metody save() modelu (lub view)
        self.cleaned_geo_data = {
            'latitude': lat,
            'longitude': lon,
            'matched_mountain': found_mountain
        }

        return image

    def save(self, commit=True):
        """Nadpisujemy save, aby uzupełnić dane w modelu."""
        instance = super().save(commit=False)
        
        # Pobieramy dane obliczone w clean_image
        geo_data = getattr(self, 'cleaned_geo_data', None)
        if geo_data:
            instance.latitude = geo_data['latitude']
            instance.longitude = geo_data['longitude']
            instance.matched_mountain = geo_data['matched_mountain']
        
        if commit:
            instance.save()
        return instance