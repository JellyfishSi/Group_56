from rest_framework import serializers
from .models import *

# Serialize the data
# Patient data serialization
class AdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = admin
        fields = ['id', 'name', 'password']

# Patient data serialization
class UserPatientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user_patient
        fields = ['id', 'name', 'id_card', 'phone', 'password', 'sex', 'age']

# Doctor data serialization
class UserDoctorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user_doctor
        fields = ['id', 'name', 'id_card', 'department_id', 'password', 'status']

# Department data serialization
class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = department
        fields = ['id', 'name', 'registration_fee', 'doctor_num']

# Drug data serialization
class MedicineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = medicine
        fields = ['id', 'name', 'price', 'unit']

# Register
class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = order
        fields = ['id', 'patient_id', 'department_id', 'readme', 'registration_fee', 'doctor_id', 'order_advice', 'medicine_list', 'total_cost', 'status', 'time']
