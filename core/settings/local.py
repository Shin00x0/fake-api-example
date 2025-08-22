from .base import *


ALLOWED_HOSTS = ["*"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    #"/var/www/static/",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files 
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"