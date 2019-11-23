from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.factories import MediaFactory, MetaFieldsFactory
import factory


class MediaAPITestCase(APITestCase):
    def setUp(self):
        self.media = MediaFactory()

    def test_get_media(self):
        self.url = reverse(
            "api:media-detail", kwargs={"uuid": self.media.uuid}
        )

        response = self.client.get(self.url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.media.name, response.data["name"])


class MetaFieldsAPITestCase(APITestCase):
    def test_add_meta_fields(self):
        media = MediaFactory()
        url = reverse(
            "api:meta-fields-create-update-multiple",
            kwargs={"uuid": media.uuid},
        )
        meta_field_1 = factory.build(dict, FACTORY_CLASS=MetaFieldsFactory)
        meta_field_2 = factory.build(dict, FACTORY_CLASS=MetaFieldsFactory)
        meta_field_1.pop("media")
        meta_field_2.pop("media")
        data = {"meta_fields": [meta_field_1, meta_field_2]}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_meta_fields(self):
        meta_field = MetaFieldsFactory()
        uuid = meta_field.media.uuid
        url = reverse("api:meta-fields-delete-multiple", kwargs={"uuid": uuid})

        data = {"meta_field_names": [meta_field.name]}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
