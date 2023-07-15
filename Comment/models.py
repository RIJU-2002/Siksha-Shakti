from django.db import models
from Post.models import Post
from authentication.models import User
# Create your models here.
def nameFile(instance,filename):
    return '/'.join(['comment',str(instance.owner.username),filename])
class Comment(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    comment=models.CharField(max_length=4000)
    comment_image=models.ImageField(upload_to=nameFile,null=True,blank=True)
    comment_date=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.comment