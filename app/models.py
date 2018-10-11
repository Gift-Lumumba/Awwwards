from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from tinymce.models import HTMLField
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Project(models.Model):
  '''
  class that contains Project properties
  '''
  title = models.CharField(max_length=40,null=True, blank=True)
  image = models.ImageField(upload_to='images/', null=True,blank=True)
  description = HTMLField()
  link = models.URLField(max_length=200)

  def save_project(self):
    self.save()

  def update_project(self):
    self.update()

  def delete_project(self):
    self.delete()


  def __str__(self):
    return self.title

class Profile(models.Model):
  '''
  class that contains user Profile properties
  '''
  profile_pic = models.ImageField(upload_to='images/',null=True, blank=True)
  bio = HTMLField()
  user = models.OneToOneField(User, on_delete=models.CASCADE,null="True")
  projects = models.ForeignKey(Project, null=True)

  def __str__(self):
    return self.bio


  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
          if created:
                  Profile.objects.create(user=instance)

  @receiver(post_save, sender=User)
  def save_user_profile(sender, instance, **kwargs):
          instance.profile.save()

  post_save.connect(save_user_profile, sender=User)

  def save_profile(self):
    self.save()

  def update_profile(self):
    self.update()

  def delete_profile(self):
    self.delete()
