#!/bin/bash

# Check if Django project exists
if [ ! -f "manage.py" ]; then
    echo "Django project not found. Please create a Django project first."
    exit 1
fi

# Prompt for app name
read -p "Enter the Django app name: " APP_NAME

# Create Django app if it doesn't exist
if [ ! -d "$APP_NAME" ]; then
    python manage.py startapp "$APP_NAME"
fi

# Create the theme app if it doesn't exist
if [ ! -d "theme" ]; then
    python manage.py startapp theme
fi

# Find settings.py and urls.py
SETTINGS_FILE=$(find . -type f -name settings.py | head -n 1)
URLS_FILE=$(find . -type f -name urls.py | head -n 1)

# Ensure 'os' is imported in settings.py
if ! grep -q "import os" "$SETTINGS_FILE"; then
    sed -i "1iimport os" "$SETTINGS_FILE"
fi

# Add app to INSTALLED_APPS in settings.py
if ! grep -q "$APP_NAME" "$SETTINGS_FILE"; then
    sed -i "/INSTALLED_APPS = \[/a \    '$APP_NAME'," "$SETTINGS_FILE"
fi

# Add Tailwind and Theme to INSTALLED_APPS
if ! grep -q "'tailwind'" "$SETTINGS_FILE"; then
    sed -i "/INSTALLED_APPS = \[/a \    'tailwind',\n    'theme',\n    'django_browser_reload'," "$SETTINGS_FILE"
fi

# Add essential settings if not present
if ! grep -q "os.path.join(BASE_DIR, 'templates')" "$SETTINGS_FILE"; then
    cat <<EOL >> "$SETTINGS_FILE"

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]
EOL
fi

if ! grep -q "STATICFILES_DIRS" "$SETTINGS_FILE"; then
    cat <<EOL >> "$SETTINGS_FILE"

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
EOL
fi

# Add static and media settings in urls.py
if ! grep -q "static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)" "$URLS_FILE"; then
    cat <<EOL >> "$URLS_FILE"

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
EOL
fi

# Install required packages using uv
uv pip install django-tailwind django-browser-reload

# Ensure the static directory exists
mkdir -p static

# Initialize Tailwind
if command -v python3 -m tailwind &> /dev/null; then
    python manage.py tailwind init
    python manage.py tailwind install
else
    echo "Tailwind is not installed. Please install it and try again."
    exit 1
fi

# Add Tailwind reload to urls.py
if ! grep -q "django_browser_reload.urls" "$URLS_FILE"; then
    sed -i "/urlpatterns = \[/a \    path(\"__reload__\", include(\"django_browser_reload.urls\"))," "$URLS_FILE"
fi

# Add app URL pattern in urls.py
if ! grep -q "path(\"$APP_NAME\", include(\"$APP_NAME.urls\"))" "$URLS_FILE"; then
    sed -i "/urlpatterns = \[/a \    path(\" $APP_NAME\", include(\"$APP_NAME.urls\"))," "$URLS_FILE"
fi

# Create urls.py in the app directory
APP_URLS_FILE="$APP_NAME/urls.py"
if [ ! -f "$APP_URLS_FILE" ]; then
    cat <<EOL > "$APP_URLS_FILE"
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
EOL
fi

# Create a basic view in views.py
if ! grep -q "def index" "$APP_NAME/views.py"; then
    cat <<EOL >> "$APP_NAME/views.py"

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
EOL
fi

# Create a template for the index view
mkdir -p "$APP_NAME/templates"
cat <<EOL > "$APP_NAME/templates/index.html"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Index</title>
</head>
<body>
    <h1>Welcome to the $APP_NAME app!</h1>
</body>
</html>
EOL

# Run migrations
python manage.py makemigrations
python manage.py migrate

echo "Django app '$APP_NAME' created and configured successfully, including the 'theme' app, 'static' directory, and URL patterns."
