# Django Gallery App

A simple Django web application for uploading and displaying images in a gallery. This project is configured for deployment on Render and supports local development with SQLite or PostgreSQL.
Features

    Upload images via the Django admin panel or a custom frontend (if implemented).
    Display images in a gallery view.
    Production-ready configuration with WhiteNoise for static/media files and PostgreSQL support.
    Deployable on Render with a free-tier PostgreSQL database.

# Prerequisites

    Python 3.8 or higher
    Django 4.x (or compatible version)
    Git and a GitHub account
    Render account (for deployment)
    PostgreSQL (for production) or SQLite (for local development)
# Installation
1. Clone the Repository
2. git clone https://github.com/sophoni-1/Photo-Share-App.git
cd Photo-Share-App
#  Create a Virtual Environment
pip install -r requirements.txt

# Configure Environment Variables

Create a .env file in the project root for local development:
DJANGO_SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3  # For local SQLite
# For PostgreSQL: DATABASE_URL=postgres://user:password@localhost:5432/dbname

# Apply Migrations
python manage.py makemigrations
python manage.py migrate

# Collect Static Files
python manage.py collectstatic --no-input

# Create a Superuser (for Admin Access)

python manage.py createsuperuser
# Project Structure
django-gallery/
├── gallery/              # Gallery app
│   ├── migrations/       # Database migrations
│   ├── templates/        # HTML templates
│   ├── models.py         # Image model
│   ├── views.py          # Gallery views
│   └── urls.py           # App-specific URLs
├── myproject/            # Django project
│   ├── settings.py       # Configuration
│   ├── urls.py           # Project URLs
│   └── wsgi.py           # WSGI entry point
├── media/                # Uploaded images
├── static/               # Static files (CSS, JS)
├── staticfiles/          # Collected static files
├── build.sh              # Build script for Render
├── requirements.txt      # Python dependencies
└── README.md             # This file

# Deployment on Render
1. Prepare Your Project

    Ensure all changes are committed to a GitHub repository.
    Verify requirements.txt, build.sh, and settings.py are configured as below.

requirements.txt:
django>=4.0
gunicorn>=20.1
psycopg2-binary>=2.9
whitenoise>=6.0
pillow>=9.0
dj-database-url>=1.0
 # build.sh

 #!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# settings.py (Key Configurations):

import os
import dj_database_url

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'default-secret')
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*.onrender.com']

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]

# Set Up a PostgreSQL Database on Render

    Log in to Render.
    Click New > PostgreSQL.
    Configure the database (e.g., name: gallery-db) and copy the Internal Database URL.
#  Deploy the Web Service

    Click New > Web Service in Render.
    Select Python and connect your GitHub repository.
    Configure:
        Build Command: ./build.sh
        Start Command: gunicorn myproject.wsgi:application
        Environment Variables:
            DJANGO_SECRET_KEY: A secure key
            DATABASE_URL: The PostgreSQL URL from step 2
            PYTHON_VERSION: e.g., 3.10
    Click Create Web Service.
    Wait for the deployment to complete and visit your app’s URL (e.g., https://your-app-name.onrender.com).

# Create an Admin User on Render

    In the Render dashboard, go to your web service’s Shell tab.
    Run:
   python manage.py createsuperuser


Access the admin panel at https://your-app-name.onrender.com/admin.

# Usage

    Upload Images: Use the admin panel (/admin) to add images to the gallery.
    View Gallery: Visit the homepage (/) to see uploaded images.
    Customize: Add frontend forms or styling by modifying gallery/templates/gallery/image_list.html.

# Troubleshooting

    Images Not Loading: Ensure MEDIA_URL and MEDIA_ROOT are set, and collectstatic was run.
    Database Errors: Verify the DATABASE_URL matches Render’s PostgreSQL URL.
    Deployment Fails: Check Render logs for missing dependencies or script errors.
    Free Tier Notes: Render’s free PostgreSQL expires after 90 days, and web services may sleep after inactivity.

# Optional Enhancements

    Image Optimization: Install django-imagekit for resizing images.
    S3 Storage: Use django-storages for scalable media storage.
    Frontend: Add Bootstrap or custom CSS for a better gallery UI.

# Contributing

    Fork the repository.
    Create a feature branch (git checkout -b feature-name).
    Commit changes (git commit -m "Add feature").
    Push to the branch (git push origin feature-name).
    Open a pull request.

License

This project is licensed under the MIT License.
