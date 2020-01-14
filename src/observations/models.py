from datetime import date

from django.contrib.gis.db import models
from django.core.validators import validate_slug, MaxValueValidator, MinValueValidator

from locations.models import Region
from birds.models import Bird


class Contributor(models.Model):
    """ Contributor details for an Observation """
    class ActivityChoices(models.TextChoices):
        UNKNOWN = '', ''
        OROKONUI = 'orokonui', 'Visiting Orokonui'
        TOURIST = 'tourist', 'Tourist'
        LOCAL = 'local', 'Local'
        SCHOOL = 'school', 'School Group'
        COMMUNITY = 'community', 'Community Group'
        TRAMPER = 'tramper', 'Tramper'
        HUNTER = 'hunter', 'Hunter'
        BIRDER = 'birder', 'Birder'
        DOC = 'doc', 'DOC Staff'
        RESEARCH = 'research', 'Researcher'
        OTHER = 'other', 'Other'

    class HeardChoices(models.TextChoices):
        UNKNOWN = '', ''
        OROKONUI = 'orokonui', 'Orokonui Ecosanctuary'
        POSTER = 'poster', 'Poster'
        BROCHURE = 'brochure', 'Brochure'
        SOCIAL = 'social', 'Social Media'
        NEWS = 'news', 'News'
        FRIEND = 'friend', 'From a friend'
        OTHER = 'other', 'Other'

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    # Optional
    activity = models.CharField(
        max_length=15,
        blank=True,
        choices=ActivityChoices.choices,
        default=ActivityChoices.UNKNOWN
    )
    heard = models.CharField(
        max_length=15,
        blank=True,
        choices=HeardChoices.choices,
        default=HeardChoices.UNKNOWN
    )

    def __str__(self):
        return self.name


class Observation(models.Model):
    """ Basic Observation instance """
    class PrecisionChoices(models.IntegerChoices):
        GPS = 10, '(10m) GPS Coordinates'
        KNOWN = 50, '(50m) Known Location'
        APPROXIMATE = 200, '(200m) Approximate Location'
        GENERAL = 1000, '(1000m) General Area'

    class ObservationTypeChoices(models.TextChoices):
        SIGHTED = 'sighted', 'Sighted'
        HEARD = 'heard', 'Heard'
        DISTANT = 'distant', 'Sighted (distant)'

    class StatusChoices(models.TextChoices):
        NEW = 'new'
        PUBLIC = 'public', 'Verified (Public)'
        PRIVATE = 'private', 'Verified (Private)'
        INVALID = 'invalid', 'Invalid (Private)'
        CAPTIVE = 'captive', 'Captive (Special)'

    # Staff only
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
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
    precision = models.PositiveIntegerField(choices=PrecisionChoices.choices)
    observation_type = models.CharField(
        max_length=15, choices=ObservationTypeChoices.choices
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
    class BandChoices(models.TextChoices):
        UNKNOWN = 'unknown', 'Couldn\'t tell'
        UNREADABLE = 'unreadable', 'Banded, unreadable'
        READABLE = 'readable', 'Banded, readable'
        UNBANDED = 'unbanded', 'Not banded'

    observation = models.ForeignKey(
        Observation, related_name='birds', on_delete=models.CASCADE
    )

    banded = models.CharField(max_length=15, choices=BandChoices.choices)

    # Optional (depends on whether bird was banded or not)
    band_combo = models.CharField(max_length=200, blank=True, null=True)
    sex_guess = models.CharField(
        max_length=15, choices=Bird.SexChoices.choices, null=True, blank=True
    )
    life_stage_guess = models.CharField(
        max_length=15,
        choices=Bird.LifeStageChoices.choices,
        null=True,
        blank=True
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
