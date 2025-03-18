from django.http import JsonResponse
from .models import *

class Action:
  # Return template for successful data request
  def success(data = ''):
    return JsonResponse({"code": 0, "data": data}, safe=False)
  # Return template for failed data requests
  def fail(data = ''):
    return JsonResponse({"code": -1, "data": data}, safe=False)
