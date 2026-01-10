# mountains/utils.py
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.distance import geodesic

def get_decimal_from_dms(dms, ref):
    # (Bez zmian - zostaw tak jak było)
    degrees = dms[0]
    minutes = dms[1]
    seconds = dms[2]
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def get_exif_data(image_file):
    """
    Przyjmuje obiekt pliku (nie ścieżkę!) i zwraca (lat, lon).
    """
    try:
        image_file.seek(0)  # Ustaw wskaźnik na początek pliku
        img = Image.open(image_file)
        img.verify()  # Weryfikacja czy to obrazek (bez wczytywania całego do RAM)
        
        # Ponowne otwarcie do odczytu danych (verify zamyka plik w niektórych wersjach)
        image_file.seek(0)
        img = Image.open(image_file)
        
        exif_data = img._getexif()
        
        if not exif_data:
            return None, None

        gps_info = {}
        for tag, value in exif_data.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_info[sub_decoded] = value[t]

        if not gps_info:
            return None, None

        lat = get_decimal_from_dms(gps_info['GPSLatitude'], gps_info['GPSLatitudeRef'])
        lon = get_decimal_from_dms(gps_info['GPSLongitude'], gps_info['GPSLongitudeRef'])
        return lat, lon
        
    except Exception as e:
        print(f"Błąd EXIF: {e}")
        return None, None

# (Funkcja check_proximity zostaje bez zmian)
def check_proximity(photo_lat, photo_lon, mountains_queryset):
    for mountain in mountains_queryset:
        mountain_coords = (mountain.latitude, mountain.longitude)
        photo_coords = (photo_lat, photo_lon)
        distance = geodesic(mountain_coords, photo_coords).meters
        if distance <= mountain.radius:
            return mountain
    return None