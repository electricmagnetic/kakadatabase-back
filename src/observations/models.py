from datetime import date

from django.contrib.gis.db import models
from django.core.validators import validate_slug, MaxValueValidator, MinValueValidator

from locations.models import Region
from birds.models import Bird

from .choices import ACTIVITY_CHOICES, HEARD_CHOICES
from .choices import STATUS_CHOICES, OBSERVATION_TYPE_CHOICES, PRECISION_CHOICES
from .choices import BAND_CHOICES, SEX_CHOICES_UNSURE, LIFE_STAGE_CHOICES_UNSURE


class Contributor(models.Model):
    """ Contributor details for an Observation """

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    # Optional
    activity = models.CharField(
        max_length=15, blank=True, choices=ACTIVITY_CHOICES, default=''
    )
    heard = models.CharField(
        max_length=15, blank=True, choices=HEARD_CHOICES, default=''
    )

    def __str__(self):
        return self.name


class Observation(models.Model):
    """ Basic Observation instance """

    # Staff only
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='new',
        help_text="Moderator: confirm verification and private/public status"
    )

    # Principal fields
    contributor = models.OneToOneField(Contributor, on_delete=models.PROTECT)

    date_sighted = models.DateField(
        validators=[MaxValueValidator(limit_value=date.today)]
    )
    time_sighted = models.TimeField()

    point_location = models.PointField()
    precision = models.PositiveIntegerField(choices=PRECISION_CHOICES)
    observation_type = models.CharField(
        max_length=15, choices=OBSERVATION_TYPE_CHOICES
    )
    number = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    # Metadata
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # Optional
    comments = models.TextField(blank=True)
    location_details = models.TextField(blank=True)
    behaviour = models.TextField(blank=True)

    # Automated
    geocode = models.CharField(max_length=200, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)

    # Staff only
    moderator_notes = models.TextField(
        blank=True,
        help_text='Moderator: Add notes here (non-public) if desired'
    )
    favourite = models.BooleanField(
        default=False, help_text="Moderator: If noteworthy observation"
    )
    confirmed = models.BooleanField(
        default=False,
        help_text='Moderator: If confirmed (known contributor or photo evidence)'
    )

    class Meta:
        ordering = [
            '-date_sighted',
            '-time_sighted',
        ]

    def __str__(self):
        return '%s %d on %s %s' % (
            self.get_observation_type_display(), self.number, self.date_sighted,
            self.time_sighted
        )


class BirdObservation(models.Model):
    """ Information specific to a bird in a observation """

    observation = models.ForeignKey(
        Observation, related_name='birds', on_delete=models.CASCADE
    )

    banded = models.CharField(max_length=15, choices=BAND_CHOICES)

    # Optional (depends on whether bird was banded or not)
    band_combo = models.CharField(max_length=200, blank=True, null=True)
    sex_guess = models.CharField(
        max_length=15, choices=SEX_CHOICES_UNSURE, null=True, blank=True
    )
    life_stage_guess = models.CharField(
        max_length=15, choices=LIFE_STAGE_CHOICES_UNSURE, null=True, blank=True
    )

    # Staff only
    bird = models.ForeignKey(
        Bird,
        related_name='observations',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    revisit = models.BooleanField(
        default=False, help_text='Moderator: tick if bird not added yet'
    )

    def __str__(self):
        return "%s [%s]" % (self.id, self.observation)
