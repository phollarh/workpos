from django.db import models
#from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields['status'] = 'admin'

        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        print(extra_fields)

        return self.create_user(email, username, password, **extra_fields)

import os

class CustomUser(AbstractBaseUser, PermissionsMixin):

	#def image_upload_to(self, instance=None):
	#	if instance:
	#		return os.path.join("accounts", self.username, instance)
	#	return None

	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=30, unique=True)
	is_active = models.BooleanField(default=True)  
	is_staff = models.BooleanField(default=False)
    #is_superuser = models.BooleanField(default=True)
	email_verified=models.BooleanField(default=True)
	
	outlet=models.ManyToManyField('Outlets', blank=True)

	STATUS = (
       
        ('Admin', 'Admin'),
        ('supervisor', 'supervisor'),
    )
	status = models.CharField(max_length=100, choices=STATUS, default='attendant')
	phone_number = PhoneNumberField(null=True, blank=True)

	objects = CustomUserManager()

  
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	def __str__(self):

		return self.username

def profile_picture_upload_path(instance, filename):
    # Generate a unique filename for the uploaded file
    unique_filename = str(uuid4())

    # Get the file's extension
    _, extension = os.path.splitext(filename)

    # Construct the upload path dynamically
    upload_path = os.path.join('pics', 'p', 'profile_pictures', unique_filename + extension)

    # Ensure that the directory structure exists
    os.makedirs(os.path.dirname(upload_path), exist_ok=True)

    return upload_path
class Profile(models.Model):
    profile = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)  
    image = models.ImageField(null=True, blank=True, upload_to='profile_picture_upload_path')
    

    def __str__(self):
        return str(self.profile.username)  # Return the username of the associated CustomUser

def create_profile(sender, instance, created, **kwargs):
    if created :
        Profile.objects.create(profile=instance)
post_save.connect(create_profile, sender=CustomUser)

class Outlets(models.Model):
	user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	name=models.CharField(max_length=50, null=False, blank=False)
	email_address=models.EmailField(max_length=50, null=True, blank=True)
	city=models.CharField(max_length=100,null=True,blank=True)
	address=models.CharField(max_length=100, null=True, blank=True)
	phone_number=models.CharField(max_length=20, null=True, blank=True)
	#staff=models.CharField(max_length=50, null=False, blank=False)
	Facebook= models.CharField(null=True, blank=True, max_length=100)
	Instagram=models.CharField(null=True, blank=True, max_length=100)
	outlet_logo=models.ImageField(null=True,blank=True,upload_to='pics/outlet_logo')
	outlet_description=models.TextField(null=True, blank=True, max_length=200)

#	Phone=models.CharField( blank=True, max_length=100)
#	City=models.CharField( blank=True, max_length=50)
#	State=models.CharField( blank=True, max_length=50)

	def __str__(self):
		return str(self.name)



# Create your models here.
class OutletStaff(models.Model):

	STATUS = (
	
		('Manager', 'Manager'),
		('Supervisor', 'Supervisor'),
		('Staff', 'Staff'),
	)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	outlet=models.ForeignKey(Outlets, on_delete=models.CASCADE)
	image = models.ImageField(null=True,blank=True,upload_to='pics/staffs/profile_picture')
	name= models.CharField(max_length=100)
	phone_number=models.CharField(max_length=30)
	address=models.CharField(max_length=100)
	email = models.EmailField(blank=True, null=True, max_length=50)
	status = models.CharField(max_length=100, choices=STATUS, default='staff')
	Employee_id=models.CharField(max_length=4)
	description = models.TextField("Description", max_length=600, default='', blank=True)


	



	def __str__(self):
		return self.name

class OutletStaffLogin(models.Model):
	user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	outlet_staff=models.OneToOneField(OutletStaff, on_delete=models.CASCADE, blank=True, null=True)
	date=models.DateTimeField(default=timezone.now)
	
	
		
def create_auto_create_outletStaffLogin(sender, instance,created, **kwargs):
     if created:
          User_Staff=OutletStaffLogin(user =instance)
          User_Staff.save()
post_save.connect(create_auto_create_outletStaffLogin, sender=CustomUser)
