from django.db import models

# Administrator class
class admin(models.Model):
    id = models.AutoField(primary_key=True) # id is created automatically and can be written manually
    name = models.CharField(max_length=45) 
    password = models.CharField(max_length=45) 

    class Meta:
        managed = False
        db_table = 'admin'

# Patient Category
class user_patient(models.Model):
    sex_choices = (
        (0, "female"),
        (1, "male")
    )
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=45) 
    id_card = models.CharField(max_length=45) 
    phone = models.CharField(max_length=45) 
    password = models.CharField(max_length=45) 
    sex = models.SmallIntegerField(choices=sex_choices) 
    age = models.SmallIntegerField() 

    class Meta:
        managed = False
        db_table = 'user_patient'

# Doctor Class
class user_doctor(models.Model):
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=45) 
    id_card = models.CharField(max_length=45) 
    department_id = models.SmallIntegerField() 
    password = models.CharField(max_length=45) 
    status = models.SmallIntegerField(default=1) 

    class Meta:
        managed = False
        db_table = 'user_doctor'

# Department Category
class department(models.Model):
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=45) 
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2) 
    doctor_num = models.SmallIntegerField(default=0) 

    class Meta:
        managed = False
        db_table = 'department'

#medicine
class medicine(models.Model):
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=45) 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    unit = models.CharField(max_length=45) 

    class Meta:
        managed = False
        db_table = 'medicine'

# Medical treatment, registration
class order(models.Model):
    id = models.AutoField(primary_key=True) 
    patient_id = models.SmallIntegerField() 
    department_id = models.SmallIntegerField() 
    readme = models.CharField(max_length=200) 
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2) 
    doctor_id = models.SmallIntegerField() 
    order_advice = models.CharField(max_length=400) 
    medicine_list = models.CharField(max_length=400)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    status = models.SmallIntegerField(default=1) 
    time = models.DateTimeField(auto_now_add=True) 

    class Meta:
        managed = False
        db_table = 'order'
