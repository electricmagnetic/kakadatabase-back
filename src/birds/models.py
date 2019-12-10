import uuid

from django.db import models

from locations.models import Area

class Bird(models.Model):
    """ Basic bird information """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    area = models.ForeignKey(Area,
        related_name='birds',
        on_delete=models.PROTECT,
    )

    primary_band = models.CharField(max_length=20)

    # Metadata
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
