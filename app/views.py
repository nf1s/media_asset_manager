# -*- coding: utf-8 -*-
"""App views Module

Module is used for creating GUI along with django templates
"""
from django.views.generic import ListView
from django.views.generic import View
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from app.models import Media, MetaFields
from django.http import HttpResponseRedirect
from app.forms import AddMetaFieldForm, EditMetaFieldForm


class MediaListView(ListView):
    template_name = "media/list.html"
    paginate_by = 6

    def get_queryset(self):
        """Method handels search and filtering of media file names"""

        query = self.request.GET.get("q")
        if query:
            return Media.objects.filter(name__icontains=query).distinct()
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


class MetaFieldEditView(FormView):
    template_name = "media/edit_meta_field.html"
    form_class = EditMetaFieldForm

    def form_valid(self, form):
        meta_field = MetaFields.objects.get(pk=self.kwargs["pk"])
        value = form.cleaned_data.get("value")
        meta_field.value = value
        meta_field.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            "app:media-detail", kwargs={"uuid": self.kwargs["uuid"]}
        )


class MetaFieldAddView(FormView):
    template_name = "media/add_meta_field.html"
    form_class = AddMetaFieldForm

    def form_valid(self, form):

        name = form.cleaned_data.get("name")
        value = form.cleaned_data.get("value")
        media = Media.objects.get(uuid=self.kwargs["uuid"])
        MetaFields.objects.create(media=media, name=name, value=value)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            "app:media-detail", kwargs={"uuid": self.kwargs["uuid"]}
        )
