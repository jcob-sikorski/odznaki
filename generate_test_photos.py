import os
import piexif  # External library required to manipulate EXIF data (pip install piexif)
from PIL import Image

# Configuration for the output directory
# This ensures we don't clutter the project root with generated images
OUTPUT_DIR = "test_photos"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def to_deg(value, loc):
    """
    Converts decimal coordinates (e.g., 49.179) into the specific Rational/DMS format 
    required by the EXIF standard.
    
    Context:
    EXIF GPS tags do not store floating point numbers directly. They store 
    Degrees, Minutes, and Seconds as tuples of (Numerator, Denominator).
    """
    if value < 0:
        loc_value = loc[1] # 'S' for South or 'W' for West
    else:
        loc_value = loc[0] # 'N' for North or 'E' for East
    
    abs_value = abs(value)
    
    # 1. Degrees (Integer)
    deg = int(abs_value)
    t1 = (deg, 1)
    
    # 2. Minutes (Integer)
    min_val = (abs_value - deg) * 60
    min_int = int(min_val)
    t2 = (min_int, 1)
    
    # 3. Seconds (Rational)
    # To maintain high precision for GPS without using floats, we multiply by 10,000
    # and store it as a fraction (e.g., 45.5 seconds becomes 455000/10000).
    sec_val = (min_val - min_int) * 60
    sec_int = int(sec_val * 10000)
    t3 = (sec_int, 10000)
    
    return (t1, t2, t3), loc_value

def create_test_photo(filename, lat=None, lon=None, color='green'):
    """
    Creates a simple colored placeholder image and injects binary GPS headers.
    
    Args:
        filename: Name of the file to save.
        lat/lon: Decimal coordinates. If None, no EXIF data is written (tests validation failure).
        color: Visual indicator for the developer to quickly identify the image type.
    """
    
    # Create a simple blank image using Pillow (PIL)
    img = Image.new('RGB', (800, 600), color=color)
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    if lat is not None and lon is not None:
        # 1. Convert decimal floats to EXIF byte structure
        lat_tuple, lat_ref = to_deg(lat, ["N", "S"])
        lon_tuple, lon_ref = to_deg(lon, ["E", "W"])
        
        # 2. Define the GPS IFD (Image File Directory) dictionary
        # We must encode the reference characters (N/S/E/W) to bytes.
        gps_ifd = {
            piexif.GPSIFD.GPSLatitudeRef: lat_ref.encode('utf-8'),
            piexif.GPSIFD.GPSLatitude: lat_tuple,
            piexif.GPSIFD.GPSLongitudeRef: lon_ref.encode('utf-8'),
            piexif.GPSIFD.GPSLongitude: lon_tuple,
        }
        
        # 3. Dump the dictionary into raw EXIF bytes
        exif_dict = {"GPS": gps_ifd}
        exif_bytes = piexif.dump(exif_dict)
        
        # 4. Save image with the injected metadata
        img.save(file_path, exif=exif_bytes)
        print(f"✅ Created: {file_path} (GPS: {lat}, {lon})")
    else:
        # Case for testing "Missing EXIF" validation error
        img.save(file_path)
        print(f"✅ Created: {file_path} (No EXIF Data)")

if __name__ == "__main__":
    print("--- Generowanie zdjęć testowych / Generating Test Photos ---")
    
    # --- SCENARIO 1: SUCCESS MATCH ---
    # Simulates a photo taken exactly at 'Rysy'.
    # Should trigger: Success message, Badge progress update.
    create_test_photo("1_rysy_match.jpg", 49.1795, 20.0881, color='green')
    
    # --- SCENARIO 2: SUCCESS MATCH (Different Peak) ---
    # Simulates a photo taken at 'Giewont'.
    # Should trigger: Success message, Distinct badge progress.
    create_test_photo("2_giewont_match.jpg", 49.2508, 19.9340, color='blue')

    # --- SCENARIO 3: LOGIC FAILURE (Proximity Check) ---
    # Simulates a photo with valid GPS (Warsaw), but too far from any defined mountain.
    # Should trigger: ValidationError "Brak dopasowania" (No match found).
    create_test_photo("3_warsaw_fail.jpg", 52.2297, 21.0122, color='red')
    
    # --- SCENARIO 4: TECHNICAL FAILURE (Missing Data) ---
    # Simulates a photo stripped of metadata (e.g., downloaded from Facebook).
    # Should trigger: ValidationError "To zdjęcie nie posiada danych GPS".
    create_test_photo("4_no_exif.jpg", color='gray')
    
    print("\nDone! Photos are located in the 'test_photos' folder.")