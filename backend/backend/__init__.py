# proj/proj/__init__.py
from ._celery import app as celery_app

__all__ = ('celery_app',)
