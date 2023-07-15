from django.db import models
from authentication.models import User
# Create your models here.
class Courses(models.Model):
    Course_name=models.CharField(null=False)
    Course_owner=models.ForeignKey(to=User,on_delete=models.CASCADE,related_name="course_name")
    Course_description=models.CharField(null=True,blank=True)
    Course_cost=models.TextField(blank=False)
    Students_purchased=models.ForeignKey(to=User,on_delete=models.CASCADE,related_name="course_students")