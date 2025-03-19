from django.test import TestCase, Client
from django.urls import reverse
from hospital.models import department, user_doctor, medicine
from decimal import Decimal
import json

class DataManagementTestCase(TestCase):
    """Test cases for hospital data management functionality"""

    def setUp(self):
        """Set up test data before each test"""
        # Set up the client
        self.client = Client()
        
        # Create an initial department for reference
        self.initial_department = department.objects.create(
            name="Cardiology",
            registration_fee=Decimal('75.00')
        )

    def test_add_department(self):
        """Test adding a new department"""
        # Since there's no direct API endpoint for adding departments in the provided code,
        # we'll test the model creation and the department listing functionality
        
        # Create a new department through the model
        new_department = department.objects.create(
            name="Neurology",
            registration_fee=Decimal('100.00')
        )
        
        # Test the department list endpoint
        response = self.client.post(reverse('departmentList'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        
        # Verify our departments are in the list
        department_data = response.json()['data']
        self.assertTrue(any(d['name'] == "Cardiology" for d in department_data))
        self.assertTrue(any(d['name'] == "Neurology" for d in department_data))
        
        # Verify the registration fee is correct
        neurology_dept = next(d for d in department_data if d['name'] == "Neurology")
        self.assertEqual(Decimal(neurology_dept['registration_fee']), Decimal('100.00'))

    def test_add_doctor(self):
        """Test adding a new doctor"""
        # Test adding a doctor through the API
        doctor_data = {
            'name': 'Dr. Johnson',
            'id_card': 'DOC54321',
            'department_id': self.initial_department.id,
            'password': 'securepass'
        }
        
        response = self.client.post(reverse('doctorAdd'), doctor_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        
        # Verify the doctor was added to the database
        new_doctor = user_doctor.objects.filter(id_card='DOC54321').first()
        self.assertIsNotNone(new_doctor)
        self.assertEqual(new_doctor.name, 'Dr. Johnson')
        self.assertEqual(new_doctor.department_id, self.initial_department.id)
        
        # Test doctor list endpoint
        response = self.client.post(reverse('doctorList'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        
        # Verify our doctor is in the list
        doctor_list = response.json()['data']
        self.assertTrue(any(d['id_card'] == 'DOC54321' for d in doctor_list))
        
        # Test duplicate doctor registration
        response = self.client.post(reverse('doctorAdd'), doctor_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], -1)  # Should fail with duplicate ID

    def test_add_medicine(self):
        """Test adding a new medicine"""
        # Test adding a medicine through the API
        medicine_data = {
            'name': 'Aspirin',
            'price': '5.99',
            'unit': 'tablet'
        }
        
        response = self.client.post(reverse('medicineAdd'), medicine_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        
        # Verify the medicine was added to the database
        new_medicine = medicine.objects.filter(name='Aspirin').first()
        self.assertIsNotNone(new_medicine)
        self.assertEqual(float(new_medicine.price), 5.99)
        self.assertEqual(new_medicine.unit, 'tablet')
        
        # Test medicine list endpoint
        response = self.client.post(reverse('medicineList'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        
        # Verify our medicine is in the list
        medicine_list = response.json()['data']
        self.assertTrue(any(m['name'] == 'Aspirin' for m in medicine_list))
        
        # Test adding a duplicate medicine
        response = self.client.post(reverse('medicineAdd'), medicine_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], -1)  # Should fail with duplicate name
        
        # Test adding a different medicine
        medicine_data2 = {
            'name': 'Amoxicillin',
            'price': '12.50',
            'unit': 'capsule'
        }
        
        response = self.client.post(reverse('medicineAdd'), medicine_data2)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        
        # Verify both medicines appear in the list
        response = self.client.post(reverse('medicineList'))
        medicine_list = response.json()['data']
        
        self.assertTrue(any(m['name'] == 'Aspirin' for m in medicine_list))
        self.assertTrue(any(m['name'] == 'Amoxicillin' for m in medicine_list))