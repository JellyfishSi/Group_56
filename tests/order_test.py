from django.test import TestCase, Client
from django.urls import reverse
from hospital.models import user_patient, department, order, user_doctor
import json


class RegistrationSystemTest(TestCase):
    """Test the patient registration system functionality"""
    
    def setUp(self):
        """Initialize test data"""
        self.client = Client()
        
        # Create a test patient
        self.test_patient = user_patient.objects.create(
            name="Test Patient",
            id_card="123456789",
            phone="1234567890",
            password="password123",
            sex=1,
            age=30
        )
        
        # Create test departments
        self.test_department1 = department.objects.create(
            name="Cardiology",
            registration_fee=50
        )
        
        self.test_department2 = department.objects.create(
            name="Neurology",
            registration_fee=60
        )
        
        # Create a test doctor
        self.test_doctor = user_doctor.objects.create(
            name="Test Doctor",
            id_card="doctor123",
            department_id=self.test_department1.id,
            password="doctor123",
            status=1
        )
        
        # Create a test order/registration
        self.test_order = order.objects.create(
            patient_id=self.test_patient.id,
            department_id=self.test_department1.id,
            readme="Test symptoms",
            registration_fee=self.test_department1.registration_fee,
            status=1
        )
    
    def test_registration_add_success(self):
        """Test successful registration creation"""
        # Register for a different department than the existing registration
        response = self.client.post(reverse('orderAdd'), {
            'user_id': self.test_patient.id,
            'department_id': self.test_department2.id,
            'readme': 'Headache and dizziness'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        
        # Verify the new registration was created in the database
        new_registration = order.objects.filter(
            patient_id=self.test_patient.id,
            department_id=self.test_department2.id
        ).first()
        
        self.assertIsNotNone(new_registration)
        self.assertEqual(new_registration.readme, 'Headache and dizziness')
        self.assertEqual(new_registration.registration_fee, self.test_department2.registration_fee)
        self.assertEqual(new_registration.status, 1)  # Status should be 1 (Registration completed)
    
    def test_registration_add_duplicate(self):
        """Test attempting to register for a department where the patient already has an active registration"""
        # Try to register for the same department
        response = self.client.post(reverse('orderAdd'), {
            'user_id': self.test_patient.id,
            'department_id': self.test_department1.id,
            'readme': 'Another symptom'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], -1)
        self.assertEqual(response.json()['data'], "No double registration")
        
        # Verify that no new registration was created
        registration_count = order.objects.filter(
            patient_id=self.test_patient.id,
            department_id=self.test_department1.id
        ).count()
        
        self.assertEqual(registration_count, 1)  # Still only one registration
    
    def test_order_list_for_patient(self):
        """Test retrieving the list of registrations for a specific patient"""
        response = self.client.post(reverse('orderList'), {
            'user_id': self.test_patient.id
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        
        # Should have one registration in the list
        registrations = response.json()['data']
        self.assertEqual(len(registrations), 1)
        self.assertEqual(registrations[0]['patient_id'], self.test_patient.id)
        self.assertEqual(registrations[0]['department_id'], self.test_department1.id)
        self.assertEqual(registrations[0]['status'], 1)
    
    def test_order_list_for_department(self):
        """Test retrieving the list of registrations for a specific department"""
        response = self.client.post(reverse('orderList'), {
            'department_id': self.test_department1.id
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        
        # Should have one registration in the list
        registrations = response.json()['data']
        self.assertEqual(len(registrations), 1)
        self.assertEqual(registrations[0]['department_id'], self.test_department1.id)
    
    def test_order_list_for_doctor(self):
        """Test retrieving the list of registrations for a specific doctor"""
        # First, assign a doctor to the registration
        self.test_order.doctor_id = self.test_doctor.id
        self.test_order.save()
        
        response = self.client.post(reverse('orderList'), {
            'doctor_id': self.test_doctor.id
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        
        # Should have one registration in the list
        registrations = response.json()['data']
        self.assertEqual(len(registrations), 1)
        self.assertEqual(registrations[0]['doctor_id'], self.test_doctor.id)
    
    def test_order_list_by_status(self):
        """Test retrieving the list of registrations with a specific status"""
        response = self.client.post(reverse('orderList'), {
            'status': 1
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        
        # Should have one registration in the list
        registrations = response.json()['data']
        self.assertEqual(len(registrations), 1)
        self.assertEqual(registrations[0]['status'], 1)
    
    def test_order_info(self):
        """Test retrieving detailed information about a specific registration"""
        response = self.client.post(reverse('orderInfo'), {
            'id': self.test_order.id
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        
        # Verify the registration details
        registration_info = response.json()['data']
        self.assertEqual(registration_info['id'], self.test_order.id)
        self.assertEqual(registration_info['patient_id'], self.test_patient.id)
        self.assertEqual(registration_info['department_id'], self.test_department1.id)
        self.assertEqual(registration_info['readme'], "Test symptoms")
        self.assertEqual(float(registration_info['registration_fee']), float(self.test_department1.registration_fee))