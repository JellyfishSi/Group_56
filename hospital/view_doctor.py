from rest_framework.decorators import api_view
from .Action import Action
from .models import *
from .serializers import *
from django.shortcuts import render


@api_view(['GET',"POST"])
# Doctor Login
def doctorLogin(request):
  # Get parameters
  id_card = request.POST.get('name')
  password = request.POST.get('password')
  # Check by ID card
  user = user_doctor.objects.filter(id_card=id_card).first()
  if not user:
    # If the user does not exist, an error message is returned
    return Action.fail("The user does not exist.")
  if user.password != password:
    # If the user exists and the password is inconsistent, an error message is returned
    return Action.fail("wrong password")
  # Login success
  # return render(request, 'admin.html')
  return Action.success(UserDoctorSerializer(user, many = False).data)

@api_view(['GET',"POST"])
# List of doctors
def doctorList(request):
  list = user_doctor.objects.all()
  arr = []
  for item in list:
    temp = {}
    temp['id'] = item.id
    temp['name'] = item.name
    temp['id_card'] = item.id_card
    temp['department_id'] = item.department_id
    temp['department_name'] = department.objects.filter(id=item.department_id).first().name
    # temp['password'] = item.password
    # temp['status'] = item.status
    arr.append(temp)
  # Login success
  return Action.success(arr)

@api_view(['GET',"POST"])
# Add Doctor
def doctorAdd(request):
  # Get parameters
  name = request.POST.get('name')
  id_card = request.POST.get('id_card')
  department_id = request.POST.get('department_id')
  password = request.POST.get('password')
  # Check if the ID number is registered
  sameIdCardUserList = user_doctor.objects.filter(id_card=id_card)
  if sameIdCardUserList.exists() == True :
    # If it is already registered, an error message is returned
    return Action.fail("Identity duplication")
  # If not registered, add to database
  doctor = user_doctor(name=name, id_card=id_card, department_id=department_id, password=password)
  doctor.save()
  # Added successfully
  return Action.success()
