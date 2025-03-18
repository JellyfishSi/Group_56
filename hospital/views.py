from django.shortcuts import render

# Page rendering
#Login Page
def login(request):
  return render(request, 'login.html')

# Administrator page: Department management
def admin_department(request):
  return render(request, 'admin_department.html')

# Admin page: Doctor management
def admin_doctor(request):
  return render(request, 'admin_doctor.html')

# Admin page: Drug Management
def admin_medicine(request):
  return render(request, 'admin_medicine.html')

# Admin page: Patient management
def admin_patient(request):
  return render(request, 'admin_patient.html')


# Patient page: Lobby
def patient_home(request):
  return render(request, 'patient_home.html')

# Patient page: Visit records
def patient_order(request):
  return render(request, 'patient_order.html')


# Doctor page: Reception room
def doctor_home(request):
  return render(request, 'doctor_home.html')

# Patient page: Admission records
def doctor_order(request):
  return render(request, 'doctor_order.html')
