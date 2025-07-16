import os

from .base import *

DEBUG = True

MEDIA_ROOT = os.path.join(BASE_DIR, "../", "mediafiles")
STATIC_ROOT = os.path.join(BASE_DIR, "../", "staticfiles")