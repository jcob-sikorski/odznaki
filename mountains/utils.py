from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.distance import geodesic

def get_decimal_from_dms(dms, ref):
    # (Bez zmian, zgodnie z prośbą)
    degrees = dms[0]
    minutes = dms[1]
    seconds = dms[2]
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def get_exif_data(image_file):
    """
    Przyjmuje obiekt pliku i zwraca (lat, lon) używając podejścia funkcyjnego.
    """
    try:
        image_file.seek(0)
        img = Image.open(image_file)
        # verify() może zamknąć plik, dlatego używamy kontekstu lub ponownego otwarcia
        exif_data = img._getexif()
        
        if not exif_data:
            return None, None

        # Funkcyjne wyciągnięcie tagu GPSInfo
        # Szukamy klucza, którego zdekodowana nazwa to "GPSInfo"
        gps_raw = next((v for k, v in exif_data.items() if TAGS.get(k) == "GPSInfo"), None)

        if not gps_raw:
            return None, None

        # Słownik składowych GPS za pomocą dictionary comprehension
        gps_info = {GPSTAGS.get(k, k): v for k, v in gps_raw.items()}

        lat = get_decimal_from_dms(gps_info['GPSLatitude'], gps_info['GPSLatitudeRef'])
        lon = get_decimal_from_dms(gps_info['GPSLongitude'], gps_info['GPSLongitudeRef'])
        
        return lat, lon
        
    except Exception as e:
        print(f"Błąd EXIF: {e}")
        return None, None

def check_proximity(photo_lat, photo_lon, mountains_queryset):
    """
    Zwraca pierwszą górę spełniającą warunek odległości lub None.
    """
    photo_coords = (photo_lat, photo_lon)

    # Używamy generatora i funkcji next(), co jest funkcyjnym odpowiednikiem break w pętli
    return next(
        (m for m in mountains_queryset 
         if geodesic((m.latitude, m.longitude), photo_coords).meters <= m.radius), 
        None
    )