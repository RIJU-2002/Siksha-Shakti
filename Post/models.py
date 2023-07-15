from django.db import models
from authentication.models import User
# Create your models here.

def nameFile(instance,filename):
    return '/'.join(['post',str(instance.owner.username),filename])
class Post(models.Model):
    owner = models.ForeignKey(to=User, related_name='posts', on_delete=models.CASCADE)
    content=models.CharField(max_length=4000)
    post_image=models.ImageField(upload_to=nameFile,null=True,blank=True)
    post_date=models.DateField(auto_now_add=True)
    category=models.CharField(max_length=3000,default=None,blank=True,null=True)
    def __str__(self):
        return self.content