from django.db import models
from django.contrib.postgres.fields import ArrayField

from birds.models import Bird
from .parsers import standardise_combo, parse_colours, parse_legs
from .validators import validate_separators, validate_combo

class BandCombo(models.Model):
    """ Basic band combo information """

    bird = models.OneToOneField(
        Bird,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='band_combo'
    )

    combo = models.CharField(max_length=255, validators=[validate_separators])

    # Automatically generated information
    colours = ArrayField(models.CharField(max_length=50), editable=False)
    leg_left = ArrayField(models.CharField(max_length=50), editable=False)
    leg_right = ArrayField(models.CharField(max_length=50), editable=False)

    # Metadata
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['bird']

    def __str__(self):
        return self.combo

    def clean(self):
        """ Run functions on each field to standardise/parse entered combo """

        self.combo = standardise_combo(self.combo)
        self.colours = parse_colours(self.combo)
        self.leg_left, self.leg_right = parse_legs(self.combo)

        validate_combo(self.combo)
