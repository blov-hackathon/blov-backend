from django.db import models
import uuid
from django.conf import settings
# Create your models here.


def upload_path(instance, filename):
    random_uuid = str(uuid.uuid4())
    name = f"{random_uuid[:2]}/{random_uuid[2:]}"
    if not len(filename.split(".")) == 1:
        name += f'.{filename.split(".")[-1]}'
    return f"donorcard/{name}"


class DonorCard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          null=False, blank=False, auto_created=True)
    cardImage = models.ImageField(upload_to=upload_path, blank=True, null=True)
    donorDate = models.DateField()
    donorType = models.CharField(max_length=10)
    donorVolume = models.IntegerField()
    donorName = models.CharField(max_length=10)
    donorBirth = models.DateField()
    donorPlace = models.CharField(max_length=10)
    cardId = models.CharField(max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
