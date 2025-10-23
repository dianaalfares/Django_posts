from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class profile(models.Model):
  user=models.OneToOneField(User,on_delete=models.CASCADE)  
  school=models.CharField(max_length=150, null=True)
  age=models.IntegerField(default=1)
  image=models.ImageField(upload_to='user/')
  token= models.CharField(null=True)
#   def __str__ (self):
    #  return  f'{self.user.first_name}{self.user.last_name} profile'
  


class post (models.Model):
 text=models.TextField(max_length= 2000, null=True)
 image=models.ImageField(upload_to='posts/')
 u=models.ForeignKey(profile,on_delete=models.CASCADE)