from rest_framework import serializers
from app.models import Media, MetaFields
from api import exceptions


class MetaFieldModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaFields
        exclude = ["id", "media"]
        read_only_fields = ["id"]


class MediaModelSerializer(serializers.ModelSerializer):
    meta_fields = MetaFieldModelSerializer(
        many=True, required=False, read_only=True
    )

    class Meta:
        model = Media
        exclude = ["id"]
        read_only_fields = ["uuid"]


class AddMultipleMetaFieldsSerializer(serializers.Serializer):
    meta_fields = MetaFieldModelSerializer(many=True)

    def add_update_multiple(self, uuid, fields):
        media = Media.objects.get(uuid=uuid)
        for field in fields:
            meta_field, _ = media.meta_fields.get_or_create(name=field["name"])
            meta_field.value = field["value"]
            meta_field.save()


class DeleteMultipleMetaFieldsSerializer(serializers.Serializer):

    meta_field_names = serializers.ListField(
        child=serializers.CharField(max_length=255), required=True
    )

    def delete_multiple(self, uuid, field_names):
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
