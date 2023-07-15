from django.db import models
from authentication.models import User
# Create your models here.

"""def get_default_image():
    return 'profile_image/default_image.avif'"""

def nameFile(instance,filename):
    return '/'.join(['images',str(instance.owner.username),filename])

class UserProfile(models.Model):
    options = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others','Others')
    )
    role=(('student','Student'),
          ('teacher','Teacher'))
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile_data')
    gender = models.CharField(
        max_length = 20,
        choices = options,
        default = 'male',
        null=False,
        blank=False
        )
    dob=models.DateField(null=True,blank=True,default=None)
    phone=models.CharField(max_length=20,null=True,blank=True)
    works_at=models.CharField(max_length=200,null=True,blank=True)
    location_x=models.FloatField(default=0.0)
    location_y=models.FloatField(default=0.0)
    studies_at=models.CharField(max_length=200,null=True,blank=True)
    profile_image=models.ImageField(upload_to=nameFile,blank=True)
    roles=models.CharField(max_length=10,choices=role,default='student',null=False,blank=False)
    no_students=models.CharField(max_length=200,null=True,blank=True)
    teach_year=models.CharField(max_length=200,null=True,blank=True)
    review=models.CharField(max_length=200,null=True,blank=True)
    salary=models.IntegerField(default=0)
    exp=models.CharField(max_length=200,null=True,blank=True)
    rank=models.IntegerField(default=0)
    
    def __str__(self):
        return self.owner.username