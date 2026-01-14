## Odznaki Górskie (Mountain Badges)

A Django web application that tracks and verifies mountain peaks visited by users. The system automatically analyzes GPS data (EXIF) from uploaded photos to verify if a user has reached a specific summit, unlocking badges and updating their dashboard.

![Dashboard Preview](https://ucarecdn.com/54dcca6f-e85f-434f-bcf4-4eb88da372c9/-/preview/807x1000/)

## Features

* **Photo Verification:** Automatically extracts Latitude/Longitude from uploaded photos.
* **Proximity Matching:** checks if the photo location is within a specific radius (e.g., 200m) of a known mountain peak.
* **Progress Dashboard:** Visual statistics of peaks climbed.
* **Interactive Map:** Leaflet.js map showing completed peaks.
* **Badge System:** Unlock badges for completing specific sets of mountains (e.g., "The Crown of Polish Mountains").
* **Admin Panel:** Easy management of Mountains, Badges, and Users.

## Prerequisites

* **Python 3.10+** (Project built using Python 3.13)
* **pip** (Python package manager)

## Installation Guide

Follow these steps to set up the project locally on your machine.

### 1. Clone the Repository

Download the project code to your local machine.

```bash
git clone <repository-url>
cd odznaki

```

### 2. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate

```

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate

```

### 3. Install Dependencies

Install the required Python packages listed in `requirements.txt`.

```bash
pip install -r requirements.txt

```

### 4. Database Setup

Initialize the SQLite database and create the necessary tables.

```bash
python manage.py migrate

```

### 5. Create an Administrator

You need a superuser account to log into the Admin Panel and add Mountains/Badges.

```bash
python manage.py createsuperuser

```

*Follow the prompts to set a username, email, and password.*

### 6. Run the Development Server

Start the Django server.

```bash
python manage.py runserver

```

Open your browser and navigate to: **[http://127.0.0.1:8000/](https://www.google.com/search?q=http://127.0.0.1:8000/)**

---

## Configuration & Usage

### 1. Setting up Data (Admin Panel)

Before users can verify peaks, you must add mountains to the system.

1. Go to `http://127.0.0.1:8000/admin/`
2. Log in with the superuser credentials created in Step 5.
3. **Add Mountains:** Click on "Mountains" and add peaks with their Name, Altitude, Latitude, and Longitude.
4. **Add Badges:** Create Badges and select which Mountains are required to unlock them.

### 2. Testing the Upload

1. Go to the homepage (Dashboard).
2. Click **"Dodaj szczyt" (Add Peak)**.
3. Upload a photo from the `test_photos/` folder (or any photo with valid GPS EXIF data).
* `1_rysy_match.jpg`: Should match Rysy (if added to DB).
* `3_warsaw_fail.jpg`: Should fail due to location mismatch.
* `4_no_exif.jpg`: Should fail due to missing GPS data.



### 3. Test Scripts

The project includes a helper script `generate_test_photos.py`. You can run this if you need to generate dummy images with specific EXIF metadata for testing purposes.

```bash
python generate_test_photos.py

```

---

## Project Structure

```text
.
├── config/                 # Main Django configuration (settings, urls)
├── mountains/              # Main application logic
│   ├── models.py           # Database models (Mountain, Photo, Badge)
│   ├── views.py            # Logic for uploading and dashboard
│   ├── utils.py            # EXIF extraction and distance calculation logic
│   └── admin.py            # Admin panel configuration
├── media/                  # User uploaded photos (do not commit actual files to git)
├── templates/              # HTML files (Bootstrap 5 + Leaflet)
├── db.sqlite3              # Local database
└── manage.py               # Django command-line utility

```

## Technologies Used

* **Backend:** Django 6.0, Python 3.13
* **Database:** SQLite3
* **Frontend:** Bootstrap 5, HTML5/CSS3
* **Mapping:** Leaflet.js, OpenStreetMap
* **Image Processing:** Pillow (PIL) for EXIF data extraction
* **Geolocation:** Geopy for distance calculation

## License

This project is for educational and hobbyist purposes.