# -*- coding: utf-8 -*-
"""App Factories Module
Factories used to make testing easier
when models are needed to be created
"""
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from app import models
from factory.fuzzy import FuzzyText


class MediaFactory(DjangoModelFactory):
    class Meta:
        model = models.Media
        django_get_or_create = ["uuid"]

    uuid = Faker("uuid4")
    name = FuzzyText("", 10, ".txt")


class MetaFieldsFactory(DjangoModelFactory):
    class Meta:
        model = models.MetaFields
        django_get_or_create = ["name"]

    name = FuzzyText("", 10, "")
    value = FuzzyText("", 10, "")
    media = SubFactory(MediaFactory)
