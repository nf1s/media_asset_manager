# -*- coding: utf-8 -*-
"""Main views module

Renders home page from README.md
"""
import os

from django.conf import settings
from django.utils.safestring import mark_safe
from django.views.generic.base import TemplateView
from markdown import markdown


class IndexView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        with open(
            os.path.join(settings.BASE_DIR, "README.md"), encoding="utf-8"
        ) as f:
            content = f.read()

        context.update({"index_content": mark_safe(markdown(content))})

        return context
