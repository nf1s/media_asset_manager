# -*- coding: utf-8 -*-
"""App urls Module
"""
from django.urls import path
from .views import (
    MediaListView,
    MediaDetailView,
    MetaFieldDeleteView,
    MetaFieldEditView,
    MetaFieldAddView,
)

app_name = "app"

urlpatterns = [
    path("", MediaListView.as_view(), name="media-list"),
    path("<str:uuid>", MediaDetailView.as_view(), name="media-detail"),
    path(
        "<str:uuid>/meta-field/delete/<int:pk>",
        MetaFieldDeleteView.as_view(),
        name="meta-field-delete",
    ),
    path(
        "<str:uuid>/meta-field/edit/<int:pk>",
        MetaFieldEditView.as_view(),
        name="meta-field-edit",
    ),
    path(
        "<str:uuid>/meta-field/add/",
        MetaFieldAddView.as_view(),
        name="meta-field-add",
    ),
]
