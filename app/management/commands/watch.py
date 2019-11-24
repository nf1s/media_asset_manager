# -*- coding: utf-8 -*-
"""Django app Watch command
"""
import time
from django.core.management.base import BaseCommand
from django.conf import settings
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from app.models import Media


class Command(BaseCommand):
    help = "Watches directory specified in settings.py"

    def handle(self, *args, **options):
        path = settings.WATCH_DIR
        observer = Observer()
        observer.schedule(WatchDogHandler(), path=path)
        observer.start()
        self.stdout.write(self.style.SUCCESS(f"Watching {path} ..."))

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()

        self.stdout.write(self.style.SUCCESS("Successfully read files"))


class WatchDogHandler(PatternMatchingEventHandler):
    patterns = ["*.txt"]

    def _get_name_from_path(self, path):
        return path.split("/")[-1]

    def on_created(self, event):
        name = self._get_name_from_path(event.src_path)
        Media.objects.create(name=name)
        print(f"{event.src_path} is {event.event_type}")

    def on_modified(self, event):
        print(f"{event.src_path} is {event.event_type}")

    def on_deleted(self, event):
        name = self._get_name_from_path(event.src_path)
        Media.objects.get(name=name).delete()
        print(f"{event.src_path} is {event.event_type}")

    def on_moved(self, event):
        # TODO:check if the file is moved to the same directory
        name = self._get_name_from_path(event.src_path)
        new_name = self._get_name_from_path(event.dest_path)
        media = Media.objects.get(name=name)
        media.name = new_name
        media.save()
        print(f"{event.src_path} is {event.event_type} to {event.dest_path}")
