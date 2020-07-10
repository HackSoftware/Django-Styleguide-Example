from django.db import models

from styleguide_example.common.models import BaseModel
from styleguide_example.common.fields import UidField

# Create your models here.
class Profile(BaseModel):
    user_id = UidField()
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    profession = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name + ' ( ' + self.profession + ' ) ( ' + self.user_id + ' )'