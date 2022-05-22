from django.db import models

# Create your models here.

ROLE_CHOICES = (
    ("User", "User"),
    ("Admin", "Admin"),
)

class User(models.Model):
    FirstName=models.CharField(max_length=50)
    LastName=models.CharField(max_length=150)
    Email=models.CharField(max_length=150)
    Password=models.CharField(max_length=150)
            
    def __str__(self):
        return self.Email

class Role(models.Model):
    Email= models.OneToOneField(User,on_delete = models.CASCADE, primary_key = True)
    Role= models.CharField(max_length = 20,choices = ROLE_CHOICES,default = 'User')