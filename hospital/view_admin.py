from rest_framework.decorators import api_view
from .Action import Action
from .models import *
from .serializers import *
from django.shortcuts import render


@api_view(['GET',"POST"])
# Administrator login
def adminLogin(request):
  # Get parameters
  name = request.POST.get('name')
  password = request.POST.get('password')
  # Query by name
  user = admin.objects.filter(name=name).first()
  if not user:
    # If the user does not exist, an error message is returned
    return Action.fail("The user does not exist.")
  if user.password != password:
    # If the user exists and the password is inconsistent, an error message is returned
    return Action.fail("wrong password")
  # Login success
  return Action.success(AdminSerializer(user, many = False).data)
