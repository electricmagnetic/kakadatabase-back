from django.db import models

from birds.models import Bird

class BandCombo(models.Model):
    """ Basic band combo information """

    bird = models.OneToOneField(
        Bird,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='band_combo'
    )

    combo = models.CharField(max_length=255)

    # Metadata
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['bird']

    def __str__(self):
        return self.combo
