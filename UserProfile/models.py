from django.db import models

# Create your models here.
class Profile(models.Model):
    profile_img = models.URLField()
    username = models.CharField()
    name = models.CharField()
    description = models.TextField()
    #fav_category = models.ManyToManyField()
    #user = models.OneToOneField()