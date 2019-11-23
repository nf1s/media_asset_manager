"""Task Queue Module
Celery is initialized in is this module
"""
from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
import os
from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "media_asset_manager.settings"
)  # DON'T FORGET TO CHANGE THIS ACCORDINGLY
queue = Celery("media_asset_manager")
queue.config_from_object("django.conf:settings", namespace="CELERY")
queue.autodiscover_tasks()

__all__ = ["queue"]
