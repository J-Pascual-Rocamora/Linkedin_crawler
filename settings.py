import os

DATABASES = {  
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DATABASE_NAME,                      # Or path to database file if using sqlite3.
        'USER': DATABASE_USER,                      # Not used with sqlite3.
        'PASSWORD': DATABASE_PASSWORD,                  # Not used with sqlite3.
        'HOST': HOST,                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': PORT,                      # Set to empty string for default. Not used with sqlite3.
    }
}

INSTALLED_APPS = (
    'Linkedin_crawler',
)