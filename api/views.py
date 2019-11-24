# -*- coding: utf-8 -*-
"""API Views Module
This Module contains controller logic for API endpoints
"""

from api import serializers
from rest_framework import generics
from app.models import Media
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q


class GetMediaByUUID(generics.RetrieveAPIView):
    """Gets Media by corresponding UUID """

    serializer_class = serializers.MediaModelSerializer

    lookup_field = "uuid"
    queryset = Media.objects.all()


class ListMedia(generics.ListAPIView):
    """Lists all media unless search url parameter contains a search string, 
    view with filter by the corresponding search parameter
    """

    serializer_class = serializers.MediaModelSerializer

    def get_queryset(self):
        """Method Overrides get_queryset to add search functionality
        
        In case of no search url parameter, all media objects will be returned
        In case of Search url parameter, search string will be used to filter
        against media.name, media.meta_fields.name and media.meta_field.value

        basically if search string matches ano of media name or its metafields 
        names or values
        these results will be returned and duplicates will be removed (if any)
        """
        query = self.kwargs.get("search", None)
        if query:
            return Media.objects.filter(
                Q(name__icontains=query)
                | Q(meta_fields__name__icontains=query)
                | Q(meta_fields__value__icontains=query)
            ).distinct()
        return Media.objects.all()


class AddUpdateMetaFields(APIView):
    """Handels add or updating meta fields of a specific media
    the cool part about this endpoint is that multiple fields can be added 
    at the sametime
    """

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
    """Handels deleting meta fields of a specific media 
    
    endpoint will accept a list of string values and will 
    delete the corresponding meta fields
    """

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
