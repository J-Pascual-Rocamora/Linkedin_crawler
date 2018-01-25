import os

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {  
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'linkedin_trial',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': '1amiaposgresspass',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

INSTALLED_APPS = (
    'Linkedin_crawler',
)

SECRET_KEY = 'REPLACE_ME'
