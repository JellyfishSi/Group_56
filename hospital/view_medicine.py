from rest_framework.decorators import api_view
from .Action import Action
from .models import *
from .serializers import *
from django.shortcuts import render

@api_view(['GET',"POST"])
# Medicine List
def medicineList(request):
  list = medicine.objects.all()
  return Action.success(MedicineSerializer(list, many = True).data)

@api_view(['GET',"POST"])
# Medicine List
def medicineStrList(request):
  medicine_list = request.POST.get('medicine_list')
  medicine_list_arr = medicine_list.split(',')
  arr = []
  for de in medicine_list_arr:
    med = medicine.objects.filter(id=de).first()
    temp = {}
    temp['id'] = med.id
    temp['name'] = med.name
    temp['price'] = med.price
    temp['unit'] = med.unit
    arr.append(temp)
  return Action.success(arr)

@api_view(['GET',"POST"])
# Add Medicine
def medicineAdd(request):
  # Get parameters
  name = request.POST.get('name')
  price = request.POST.get('price')
  unit = request.POST.get('unit')
  # Query
  sameIdCardUserList = medicine.objects.filter(name=name)
  if sameIdCardUserList.exists() == True :
    # If it is already registered, an error message is returned
    return Action.fail("already exist")
  # If not registered, add to database
  new_medicine = medicine(name=name, price=price, unit=unit)
  new_medicine.save()
  # Added successfully
  return Action.success()
