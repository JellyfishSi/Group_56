from django.test import TestCase, Client
from django.urls import reverse
from hospital.models import user_doctor, user_patient, department, order, medicine
from decimal import Decimal

class DoctorConsultationTestCase(TestCase):
    """Test cases for doctor consultation process"""

    def setUp(self):
        """Set up test data before each test"""
        # Create a test department
        self.department = department.objects.create(
            name="General Medicine",
            registration_fee=Decimal('50.00'),
        )
        
        # Create a test doctor
        self.doctor = user_doctor.objects.create(
            name="Dr. Smith",
            id_card="DOC12345",
            department_id=self.department.id,
            password="password123",
            status=1
        )
        
        # Create a test patient
        self.patient = user_patient.objects.create(
            name="John Doe",
            id_card="PAT12345",
            phone="1234567890",
            password="password123",
            sex=1,
            age=30
        )
        
        # Create a test medicine
        self.medicine1 = medicine.objects.create(
            name="Paracetamol",
            price=Decimal('10.00'),
            unit="tablet"
        )
        
        self.medicine2 = medicine.objects.create(
            name="Ibuprofen",
            price=Decimal('15.00'),
            unit="tablet"
        )
        
        # Create a test order (registration)
        self.order = order.objects.create(
            patient_id=self.patient.id,
            department_id=self.department.id,
            readme="Fever and headache",
            registration_fee=self.department.registration_fee,
            status=1  # Registration completed status
        )
        
        # Set up the client
        self.client = Client()

    def test_doctor_consultation_process(self):
        """Test the doctor's ability to access and process a patient's consultation"""
        # Test getting the order for consultation
        response = self.client.post(reverse('orderList'), {
            'department_id': self.department.id,
            'status': 1
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)  # Success code
        
        # Verify the order details are correct
        order_data = response.json()['data']
        self.assertTrue(len(order_data) > 0)
        self.assertEqual(order_data[0]['patient_name'], self.patient.name)
        self.assertEqual(order_data[0]['department_name'], self.department.name)
        
        # Test getting order info
        response = self.client.post(reverse('orderInfo'), {
            'id': self.order.id
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data']['readme'], "Fever and headache")

    def test_prescribing_medicine(self):
        """Test doctor's ability to prescribe medicine"""
        # Get medicine list
        response = self.client.post(reverse('medicineList'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        
        # Check that our test medicines are in the list
        medicine_data = response.json()['data']
        self.assertTrue(any(m['name'] == "Paracetamol" for m in medicine_data))
        self.assertTrue(any(m['name'] == "Ibuprofen" for m in medicine_data))
        
        # Create medicine list for prescription
        medicine_list = f"{self.medicine1.id},{self.medicine2.id}"
        
        # Verify medicine string list functionality
        response = self.client.post(reverse('medicineStrList'), {
            'medicine_list': medicine_list
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(len(response.json()['data']), 2)

    def test_consultation_completion(self):
        """Test completing a consultation with prescription and advice"""
        # Complete the consultation
        response = self.client.post(reverse('orderFinish'), {
            'id': self.order.id,
            'doctor_id': self.doctor.id,
            'order_advice': "Take medication twice daily with food",
            'medicine_list': f"{self.medicine1.id},{self.medicine2.id}"
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        
        # Check that the order status has been updated
        updated_order = order.objects.get(id=self.order.id)
        self.assertEqual(updated_order.status, 2)  # Consultation completed status
        self.assertEqual(updated_order.doctor_id, self.doctor.id)
        self.assertEqual(updated_order.order_advice, "Take medication twice daily with food")
        self.assertEqual(updated_order.medicine_list, f"{self.medicine1.id},{self.medicine2.id}")
        
        # Check the total cost calculation
        expected_cost = self.department.registration_fee + self.medicine1.price + self.medicine2.price
        self.assertEqual(updated_order.total_cost, expected_cost)
        
        # Test attempting to complete an already completed consultation
        response = self.client.post(reverse('orderFinish'), {
            'id': self.order.id,
            'doctor_id': self.doctor.id,
            'order_advice': "Updated advice",
            'medicine_list': f"{self.medicine1.id}"
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], -1)  # Failure code