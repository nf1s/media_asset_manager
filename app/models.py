# -*- coding: utf-8 -*-
"""App Models Module
"""
from django.db import models
from uuid import uuid4


class Media(models.Model):
    uuid = models.CharField(
        max_length=255, blank=False, unique=True, default=uuid4
    )
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class MetaFields(models.Model):
    media = models.ForeignKey(
        Media,
        related_name="meta_fields",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}: {self.value}"
