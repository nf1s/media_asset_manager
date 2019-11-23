from django.urls import path
from .views import IndexView, MediaDetailView, MetaFieldDeleteView

app_name = "app"

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("<str:uuid>", MediaDetailView.as_view(), name="media-detail"),
    path(
        "<str:uuid>/meta-field/<int:pk>",
        MetaFieldDeleteView.as_view(),
        name="meta-field-delete",
    ),
]
