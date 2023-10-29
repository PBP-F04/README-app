import uuid
from django.db import models
from authentication.models import User

app_name = 'UserProfile'

# Create your models here.
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_image = models.URLField()
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    favorite_category = models.ForeignKey('KatalogBuku.Category', related_name='profiles', blank=True, null=True, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
