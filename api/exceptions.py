"""API Exceptions Module
    All exceptions related to API endpoints are handeld here
"""
from rest_framework.exceptions import APIException


class DoesNotExist(APIException):
    status_code = 400
    default_detail = "Error: Does Not Exist"
    default_code = "Does Not exist"
