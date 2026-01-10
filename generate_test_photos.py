import os
import piexif
from PIL import Image

# Konfiguracja folderu wyjściowego
OUTPUT_DIR = "test_photos"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def to_deg(value, loc):
    """
    Konwertuje współrzędne dziesiętne (np. 49.179) na format wymagany przez EXIF
    (krotki liczb całkowitych: stopnie, minuty, sekundy).
    """
    if value < 0:
        loc_value = loc[1] # S lub W
    else:
        loc_value = loc[0] # N lub E
    
    abs_value = abs(value)
    deg = int(abs_value)
    t1 = (deg, 1)
    
    min_val = (abs_value - deg) * 60
    min_int = int(min_val)
    t2 = (min_int, 1)
    
    sec_val = (min_val - min_int) * 60
    # Mnożymy przez 10000, aby zachować precyzję jako liczbę całkowitą
    sec_int = int(sec_val * 10000)
    t3 = (sec_int, 10000)
    
    return (t1, t2, t3), loc_value

def create_test_photo(filename, lat=None, lon=None, color='green'):
    """Tworzy obrazek i dodaje do niego dane GPS (jeśli podano)."""
    
    img = Image.new('RGB', (800, 600), color=color)
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    if lat is not None and lon is not None:
        # Konwersja danych
        lat_tuple, lat_ref = to_deg(lat, ["N", "S"])
        lon_tuple, lon_ref = to_deg(lon, ["E", "W"])
        
        gps_ifd = {
            piexif.GPSIFD.GPSLatitudeRef: lat_ref.encode('utf-8'),
            piexif.GPSIFD.GPSLatitude: lat_tuple,
            piexif.GPSIFD.GPSLongitudeRef: lon_ref.encode('utf-8'),
            piexif.GPSIFD.GPSLongitude: lon_tuple,
        }
        
        exif_dict = {"GPS": gps_ifd}
        exif_bytes = piexif.dump(exif_dict)
        img.save(file_path, exif=exif_bytes)
        print(f"✅ Utworzono: {file_path} (GPS: {lat}, {lon})")
    else:
        img.save(file_path)
        print(f"✅ Utworzono: {file_path} (Bez EXIF)")

if __name__ == "__main__":
    print("--- Generowanie zdjęć testowych ---")
    
    # 1. Rysy (Trafienie) - Zakładając, że Rysy w bazie mają ok. 49.1795, 20.0881
    create_test_photo("1_rysy_match.jpg", 49.1795, 20.0881, color='green')
    
    # 2. Giewont (Inny szczyt) - Zakładając, że jest w bazie
    create_test_photo("2_giewont_match.jpg", 49.2508, 19.9340, color='blue')

    # 3. Warszawa (Pudło - daleko od gór)
    create_test_photo("3_warsaw_fail.jpg", 52.2297, 21.0122, color='red')
    
    # 4. Zdjęcie bez EXIF (Błąd walidacji)
    create_test_photo("4_no_exif.jpg", color='gray')
    
    print("\nGotowe! Zdjęcia znajdują się w folderze 'test_photos'.")