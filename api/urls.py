from django.urls import path
from api.views import (
    GetMediaByUUID,
    ListMedia,
    AddUpdateMetaFields,
    DeleteMetaFields,
)
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = "api"

schema_view = get_schema_view(
    openapi.Info(
        title="Media Asset Manager API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("media/", ListMedia.as_view(), name="media-list"),
    path("media/<str:uuid>", GetMediaByUUID.as_view(), name="media-detail"),
    path(
        "media/<str:uuid>/meta-fields/create-multiple",
        AddUpdateMetaFields.as_view(),
        name="meta-fields-create-update-multiple",
    ),
    path(
        "media/<str:uuid>/meta-fields/delete-multiple",
        DeleteMetaFields.as_view(),
        name="meta-fields-delete-multiple",
    ),
]
