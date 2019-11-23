from django.urls import path
from .views import MediaListView, MediaDetailView, MetaFieldDeleteView

app_name = "app"

urlpatterns = [
    path("", MediaListView.as_view(), name="media-list"),
    path("<str:uuid>", MediaDetailView.as_view(), name="media-detail"),
    path(
        "<str:uuid>/meta-field/<int:pk>",
        MetaFieldDeleteView.as_view(),
        name="meta-field-delete",
    ),
]
