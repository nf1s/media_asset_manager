# -*- coding: utf-8 -*-
"""Media Asset Manager URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from .views import IndexView

urlpatterns = [
    # Url structure is based on Ahmed's order cancellation ms
    path("admin/", admin.site.urls),
    path("media/", include("app.urls")),
    path("api/", include("api.urls")),
    path("", IndexView.as_view(), name="index"),
]
name = "media asset manager".title()

admin.site.site_header = f"{name} Admin"
admin.site.site_title = f"{name} Admin"
admin.site.index_title = f"Welcome to {name}"
