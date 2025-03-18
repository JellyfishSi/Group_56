from rest_framework.decorators import api_view
from .Action import Action
from .models import *
from .serializers import *
from django.shortcuts import render


@api_view(['GET',"POST"])
# Get a list of departments
def departmentList(request):
  # Get parameters
  # name = request.POST.get('name')
  # Query by name
  # user = department.objects.filter(name=name).first()
  list = department.objects.all()
  for item in list:
    item.doctor_num = user_doctor.objects.filter(department_id=item.id).count()
  # Login success
  return Action.success(DepartmentSerializer(list, many = True).data)
  # return Action.success(list)
