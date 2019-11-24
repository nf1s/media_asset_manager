# -*- coding: utf-8 -*-
"""App Forms Module
"""
from django.forms import ModelForm
from app.models import MetaFields


class AddMetaFieldForm(ModelForm):
    class Meta:
        model = MetaFields
        fields = ["name", "value"]


class EditMetaFieldForm(ModelForm):
    class Meta:
        model = MetaFields
        fields = ["value"]
