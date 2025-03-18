from rest_framework.views import exception_handler
from django.db import DatabaseError
from rest_framework.response import Response
from rest_framework import status
import logging

def custom_exception_handler(exc, context):
    """
    Custom exception handling classes
    :param exc: exception handling object when an exception occurs
    :param context: The context in which the exception is thrown
    :return: Response Indicates the response object
    """
    response = exception_handler(exc, context)
    if response is None:
        print(exc)

    return Response({"code":500, "data": 'Server error occurred'})
