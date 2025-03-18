from rest_framework.decorators import api_view
from .Action import Action
from .models import *
from .serializers import *

@api_view(['GET',"POST"])
# Patient Registration
def patientRegister(request):
  # Get parameters
  name = request.POST.get('name')
  id_card = request.POST.get('id_card')
  phone = request.POST.get('phone')
  password = request.POST.get('password')
  sex = request.POST.get('sex')
  age = request.POST.get('age')
  # Check if the ID number is registered
  sameIdCardUserList = user_patient.objects.filter(id_card=id_card)
  if sameIdCardUserList.exists() == True :
    # If it is already registered, an error message is returned
    return Action.fail("you are registered")
  # If not registered, add to database
  user = user_patient(name=name, id_card=id_card, phone=phone, password=password, sex=sex, age=age)
  user.save()
  return Action.success()

@api_view(['GET',"POST"])
# Patient Login
def patientLogin(request):
  # Get parameters
  id_card = request.POST.get('name')
  password = request.POST.get('password')
  # Search by ID number
  user = user_patient.objects.filter(id_card=id_card).first()
  if not user:
    # If the user does not exist, an error message is returned
    return Action.fail("The user does not exist.")
  if user.password != password:
    # If the user exists and the password is inconsistent, an error message is returned
    return Action.fail("wrong password")
  # Login success
  return Action.success(UserPatientSerializer(user, many = False).data)

@api_view(['GET',"POST"])
# Patient List
def patientList(request):
  return Action.success(UserPatientSerializer(user_patient.objects.all(), many = True).data)
