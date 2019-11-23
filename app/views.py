from django.views.generic import ListView
from django.views.generic import View

from django.urls import reverse_lazy
from app.models import Media, MetaFields
from django.db.models import Q
from django.http import HttpResponseRedirect


class MediaListView(ListView):
    template_name = "media/list.html"
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Media.objects.filter(
                Q(name__icontains=query)
                | Q(meta_fields__name__icontains=query)
                | Q(meta_fields__value__icontains=query)
            ).distinct()
        else:
            return Media.objects.all()


class MediaDetailView(ListView):
    template_name = "media/detail.html"

    def get_queryset(self):
        media = Media.objects.get(uuid=self.kwargs["uuid"])
        return media.meta_fields.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"media_uuid": self.kwargs["uuid"]})
        return context


class MetaFieldDeleteView(View):
    def get(self, *args, **kwargs):
        MetaFields.objects.get(pk=self.kwargs["pk"]).delete()
        return HttpResponseRedirect(
            reverse_lazy(
                "app:media-detail", kwargs={"uuid": self.kwargs["uuid"]}
            )
        )
