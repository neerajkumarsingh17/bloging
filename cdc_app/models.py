from operator import truediv
from random import choices
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import pdb


# Create your models here.
# Rajat's models
class Profile(models.Model):

    ROLE_CHOICES = (
        ('SuperAdmin','SuperAdmin'),
        ('Staff','Staff'),
        ('Observer','Observer'),
    )

    GENDER_CHOICES = (
        ('male','male'),
        ('female','female'),
        ('-','-'),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='profile',unique=True)
    emp_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100,blank=True)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES)
    gender = models.CharField(choices=GENDER_CHOICES, default="-", max_length=100)
    designation = models.CharField(max_length=100)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.first_name + ' ' + self.last_name


class School(models.Model):
    school_code = models.CharField(max_length=100)
    school_name = models.CharField(max_length=100)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.school_name

 
class ProfileSchool(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    school = models.ForeignKey(School,on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.profile) + ' -> ' + str(self.school)
    



# Saumya's models

# class Location(models.Model):


#     address = models.TextField()
#     city = models.CharField(max_length=100, )
#     state = models.CharField(choices=state_choices,max_length=100, )
#     zipcode = models.IntegerField()
#     country = models.CharField(max_length=100, default = 'India')
#     created_datetime = models.DateTimeField(auto_now_add=True)
#     modified_datetime = models.DateTimeField(auto_now=True)
#     def __str__(self):
#         return self.city + '-' + self.state

#     class Meta:
#         verbose_name_plural = "Locations"

class Company(models.Model):
    state_choices = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))
  

    spoc = models.ForeignKey(Profile,on_delete=models.CASCADE, null = True)
    name = models.CharField(max_length=100, )
    website = models.URLField(max_length=100,)
    contact = models.CharField(max_length=100, )
    email = models.EmailField()
    phone = models.IntegerField()
    position = models.CharField(max_length=50, default='')
    address = models.TextField(default='')
    city = models.CharField(max_length=100,default="" )
    state = models.CharField(choices=state_choices,max_length=100,default="" )
    zipcode = models.IntegerField(null=True)
    country = models.CharField(max_length=100, default = 'India')
    #location = models.ForeignKey(Location, on_delete = models.CASCADE,default='')
    sector = models.CharField(max_length=100, default='')
    company_turnover = models.FloatField(max_length=100, default='' )
    approximate_manpower = models.IntegerField(max_length=100, default='')
    is_approved = models.BooleanField(default=False)

    # is_approved = models.BooleanField(default=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    def approve(self):
        self.is_approved = True

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"

class Course(models.Model):
    name = models.CharField(max_length=100)

    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Courses"

class Client(models.Model):
    from datetime import datetime
    """
    Model for batches
    """
    pdc_choices = (
        ('yes', 'yes'),
        ('no', 'no'),
    )
    consideration_choices = (('approved','approved'), 
                            ('disapproved','disapproved'), 
                            ('pending','pending'))

    company = models.ForeignKey(Company, related_name='clients', on_delete=models.CASCADE,)
    date_of_entry = models.DateField()
    spoc = models.ForeignKey(Profile, related_name='clients', on_delete=models.CASCADE)
    projected_no_of_students = models.IntegerField()
    school = models.ManyToManyField(School, related_name='clients')
    course = models.ManyToManyField(Course, related_name='clients')
    lead_source = models.CharField(max_length=200)
    remarks = models.TextField()
    date_of_first_contact = models.DateField(default=datetime.now)
    date_of_last_contact = models.DateField(default=datetime.now)
    lead_status = models.TextField()
    next_action = models.TextField()
    outcome = models.CharField(max_length=200)
    placement_drive_conducted = models.CharField(choices=pdc_choices, default="no", max_length=50)
    internship_drive_conducted = models.CharField(choices=pdc_choices, default="no", max_length=50)
    no_of_students_hired =  models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)

    consideration_status = models.CharField(choices=consideration_choices, default="pending", max_length=100)

    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
    
        return self.company.name

    class Meta:
        verbose_name_plural = "Clients"
