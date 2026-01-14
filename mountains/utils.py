# mountains/utils.py
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.distance import geodesic

def get_decimal_from_dms(dms, ref):
    """
    Helper to convert Degrees/Minutes/Seconds (EXIF format) to Decimal Degrees.
    """
    degrees = dms[0]
    minutes = dms[1]
    seconds = dms[2]
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    
    # Adjust sign based on hemisphere (South or West are negative)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def get_exif_data(image_file):
    """
    Extracts GPS coordinates from an image file object using a functional approach.
    Returns: (latitude, longitude) or (None, None)
    """
    try:
        # Reset file pointer to beginning to ensure we read the whole file
        image_file.seek(0)
        img = Image.open(image_file)
        
        # extracting raw EXIF data
        exif_data = img._getexif()
        
        if not exif_data:
            return None, None

        # Functional extraction of the specific "GPSInfo" tag.
        # We iterate over the dictionary to find the key corresponding to "GPSInfo".
        gps_raw = next((v for k, v in exif_data.items() if TAGS.get(k) == "GPSInfo"), None)

        if not gps_raw:
            return None, None

        # Decode GPS specific tags (e.g., converting tag IDs to names like 'GPSLatitude')
        gps_info = {GPSTAGS.get(k, k): v for k, v in gps_raw.items()}

        # Convert DMS components to decimal coordinates
        lat = get_decimal_from_dms(gps_info['GPSLatitude'], gps_info['GPSLatitudeRef'])
        lon = get_decimal_from_dms(gps_info['GPSLongitude'], gps_info['GPSLongitudeRef'])
        
        return lat, lon
        
    except Exception as e:
        print(f"EXIF Error: {e}")
        return None, None

def check_proximity(photo_lat, photo_lon, mountains_queryset):
    """
    Determines if the photo coordinates are within the radius of any known mountain.
    Returns the first matching Mountain object or None.
    """
    photo_coords = (photo_lat, photo_lon)

    # Uses a generator expression with next() for efficiency.
    # This stops iteration as soon as the first match is found (functional equivalent of a loop break).
    return next(
        (m for m in mountains_queryset 
         if geodesic((m.latitude, m.longitude), photo_coords).meters <= m.radius), 
        None
    )