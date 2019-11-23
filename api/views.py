from api import serializers
from rest_framework import generics
from app.models import Media
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


class GetMediaByUUID(generics.RetrieveAPIView):

    serializer_class = serializers.MediaModelSerializer

    lookup_field = "uuid"
    queryset = Media.objects.all()


class ListMedia(generics.ListAPIView):

    serializer_class = serializers.MediaModelSerializer
    queryset = Media.objects.all()


class AddUpdateMetaFields(APIView):
    @swagger_auto_schema(
        request_body=serializers.AddMultipleMetaFieldsSerializer(),
        operation_id="meta_fields_create_update",
        responses={
            status.HTTP_200_OK: serializers.AddMultipleMetaFieldsSerializer
        },
    )
    def post(self, request: Request, **kwargs):
        serializer = serializers.AddMultipleMetaFieldsSerializer(
            data=request.data
        )
        if not serializer.is_valid():
            pass

        serializer.add_update_multiple(
            kwargs["uuid"], request.data["meta_fields"]
        )
        return Response(data=serializer.data)


class DeleteMetaFields(APIView):
    @swagger_auto_schema(
        request_body=serializers.DeleteMultipleMetaFieldsSerializer(),
        operation_id="meta_fields_delete",
        responses={
            status.HTTP_200_OK: serializers.DeleteMultipleMetaFieldsSerializer
        },
    )
    def post(self, request: Request, **kwargs):
        serializer = serializers.DeleteMultipleMetaFieldsSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.delete_multiple(
                kwargs["uuid"], request.data["meta_field_names"]
            )
            return Response(data=serializer.data)

        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"errors": serializer.errors},
        )
