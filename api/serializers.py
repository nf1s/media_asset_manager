# -*- coding: utf-8 -*-
"""API Apps Module
This Module contains the models used for serializing data
for all endpoints
"""

from rest_framework import serializers
from app.models import Media, MetaFields
from api import exceptions


class MetaFieldModelSerializer(serializers.ModelSerializer):
    """Serializes data for MetaFields Model"""

    class Meta:
        model = MetaFields
        exclude = ["id", "media"]
        read_only_fields = ["id"]


class MediaModelSerializer(serializers.ModelSerializer):
    """Serializes data for Media Model and nests MetaFields"""

    meta_fields = MetaFieldModelSerializer(
        many=True, required=False, read_only=True
    )

    class Meta:
        model = Media
        exclude = ["id"]
        read_only_fields = ["uuid"]


class AddMultipleMetaFieldsSerializer(serializers.Serializer):
    """Serializer handles adding and/or updating multiple meta field values"""

    meta_fields = MetaFieldModelSerializer(many=True)

    def add_update_multiple(self, uuid: str, fields: dict):
        """Method adds or updates multiple meta fields to
        
        Args:
            uuid (str): media uuid
            fields (list[dict]): List of dicts containing meta field values
            e.g [{"name":"field_1", "value":"value_1"}]
        """
        media = Media.objects.get(uuid=uuid)
        for field in fields:
            meta_field, _ = media.meta_fields.get_or_create(name=field["name"])
            meta_field.value = field["value"]
            meta_field.save()


class DeleteMultipleMetaFieldsSerializer(serializers.Serializer):
    """Serializer deletes mutiple meta fields by their keys"""

    meta_field_names = serializers.ListField(
        child=serializers.CharField(max_length=255), required=True
    )

    def delete_multiple(self, uuid: str, field_names: list):
        """Method deletes multiple meta field by their keys or
        
        Args:
            uuid (str): media uuid
            field_names (list[str]): List of field names to be deleted
        
        Raises:
            exceptions.DoesNotExist: if there are field names that do not exit in database
        """
        media = Media.objects.get(uuid=uuid)
        wrong_field_names = []
        for name in field_names:
            try:
                media.meta_fields.get(media=media, name=name).delete()
            except MetaFields.DoesNotExist:
                wrong_field_names.append(name)

        if wrong_field_names:
            message = "media does not have meta fields with these names"
            raise exceptions.DoesNotExist(
                f"{message} {str(wrong_field_names)}"
            )
