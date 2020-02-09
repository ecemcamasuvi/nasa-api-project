from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE,primary_key=True)
    user_image = models.FileField(blank = True,null = True,verbose_name="Please choose profile photo")