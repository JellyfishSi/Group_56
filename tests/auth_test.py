from django.test import TestCase, Client
from django.urls import reverse
from hospital.models import user_patient, user_doctor, admin


class PatientAuthenticationTest(TestCase):
    """Test patient authentication functionality"""
    
    def setUp(self):
        """Initialize test data"""
        self.client = Client()
        # Create a test patient account
        self.test_patient = user_patient.objects.create(
            name="Test Patient",
            id_card="123456789",
            phone="1234567890",
            password="password123",
            sex=1,
            age=30
        )
    
    def test_patient_login_success(self):
        """Test successful patient login"""
        response = self.client.post(reverse('patientLogin'), {
            'name': '123456789',  # Using id_card as login name
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)  # Success code is 0
        self.assertEqual(response.json()['data']['name'], "Test Patient")
    
    def test_patient_login_wrong_password(self):
        """Test patient login with incorrect password"""
        response = self.client.post(reverse('patientLogin'), {
            'name': '123456789',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], -1)  # Failure code is -1
        self.assertEqual(response.json()['data'], "wrong password")
    
    def test_patient_login_nonexistent_user(self):
        """Test patient login with non-existent account"""
        response = self.client.post(reverse('patientLogin'), {
            'name': 'nonexistent',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], -1)
        self.assertEqual(response.json()['data'], "The user does not exist.")
    
    def test_patient_register_success(self):
        """Test successful patient registration"""
        response = self.client.post(reverse('patientRegister'), {
            'name': 'New Patient',
            'id_card': '987654321',
            'phone': '9876543210',
            'password': 'newpassword',
            'sex': '1',
            'age': '25'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        
        # Verify that the new patient was created in the database
        new_patient = user_patient.objects.get(id_card='987654321')
        self.assertEqual(new_patient.name, 'New Patient')
        self.assertEqual(new_patient.age, 25)
    
    def test_patient_register_duplicate_id(self):
        """Test patient registration with a duplicate ID card number"""
        response = self.client.post(reverse('patientRegister'), {
            'name': 'Duplicate Patient',
            'id_card': '123456789',  # Existing ID card number
            'phone': '9876543210',
            'password': 'newpassword',
            'sex': '1',
            'age': '25'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], -1)
        self.assertEqual(response.json()['data'], "you are registered")


class DoctorAuthenticationTest(TestCase):
    """Test doctor authentication functionality"""
    
    def setUp(self):
        """Initialize test data"""
        self.client = Client()
        # Create a test doctor account
        self.test_doctor = user_doctor.objects.create(
            name="Test Doctor",
            id_card="doctor123",
            department_id=1,
            password="doctor123",
            status=1
        )
    
    def test_doctor_login_success(self):
        """Test successful doctor login"""
        response = self.client.post(reverse('doctorLogin'), {
            'name': 'doctor123',  # Using id_card as login name
            'password': 'doctor123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data']['name'], "Test Doctor")
    
    def test_doctor_login_wrong_password(self):
        """Test doctor login with incorrect password"""
        response = self.client.post(reverse('doctorLogin'), {
            'name': 'doctor123',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], -1)
        self.assertEqual(response.json()['data'], "wrong password")
    
    def test_doctor_login_nonexistent_user(self):
        """Test doctor login with non-existent account"""
        response = self.client.post(reverse('doctorLogin'), {
            'name': 'nonexistent',
            'password': 'doctor123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], -1)
        self.assertEqual(response.json()['data'], "The user does not exist.")


class AdminAuthenticationTest(TestCase):
    """Test administrator authentication functionality"""
    
    def setUp(self):
        """Initialize test data"""
        self.client = Client()
        # Create a test admin account
        self.test_admin = admin.objects.create(
            name="admin",
            password="admin123"
        )
    
    def test_admin_login_success(self):
        """Test successful admin login"""
        response = self.client.post(reverse('adminLogin'), {
            'name': 'admin',
            'password': 'admin123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data']['name'], "admin")
    
    def test_admin_login_wrong_password(self):
        """Test admin login with incorrect password"""
        response = self.client.post(reverse('adminLogin'), {
            'name': 'admin',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], -1)
        self.assertEqual(response.json()['data'], "wrong password")
    
    def test_admin_login_nonexistent_user(self):
        """Test admin login with non-existent account"""
        response = self.client.post(reverse('adminLogin'), {
            'name': 'nonexistent',
            'password': 'admin123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], -1)
        self.assertEqual(response.json()['data'], "The user does not exist.")