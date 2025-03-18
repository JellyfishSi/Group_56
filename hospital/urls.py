# from django.contrib import admin
from hospital import view_admin
from hospital import view_patient
from hospital import view_doctor
from hospital import view_medicine
from hospital import view_department
from hospital import view_order
from django.urls import path
from django.shortcuts import redirect
from hospital import views

urlpatterns = [
    # The root path redirects to the login page
    path('', lambda request: redirect('login/')),

    # Page Request
    path('login/', views.login, name='login'),
    path('admin/', views.admin_department, name='admin'),
    path('admin_department/', views.admin_department),
    path('admin_doctor/', views.admin_doctor),
    path('admin_medicine/', views.admin_medicine),
    path('admin_patient/', views.admin_patient),

    path('patient/', views.patient_home, name='patient_home'),
    path('patient_home/', views.patient_home),
    path('patient_order/', views.patient_order),

    path('doctor/', views.doctor_order, name='doctor_order'),
    path('doctor_home/', views.doctor_home),
    path('doctor_order/', views.doctor_order),

    # Data Request

    # Administrator
    path('adminLogin', view_admin.adminLogin, name='adminLogin'),
    path('departmentList', view_department.departmentList, name='departmentList'),
    path('doctorList', view_doctor.doctorList, name='doctorList'),
    path('doctorAdd', view_doctor.doctorAdd, name='doctorAdd'),
    path('patientList', view_patient.patientList, name='patientList'),
    path('patientAdd', view_patient.patientRegister, name='patientAdd'),
    
    # Medicine
    path('medicineList', view_medicine.medicineList, name='medicineList'),
    path('medicineStrList', view_medicine.medicineStrList, name='medicineStrList'),
    path('medicineAdd', view_medicine.medicineAdd, name='medicineAdd'),
    
    # Patient
    path('patientRegister', view_patient.patientRegister, name='patientRegister'),
    path('patientLogin', view_patient.patientLogin, name='patientLogin'),
    
    # order
    path('orderAdd', view_order.orderAdd, name='orderAdd'),
    path('orderList', view_order.orderList, name='orderList'),
    path('orderInfo', view_order.orderInfo, name='orderInfo'),
    path('orderFinish', view_order.orderFinish, name='orderFinish'),

    # doctor
    path('doctorLogin', view_doctor.doctorLogin, name='doctorLogin'),
]
