import uuid
from datetime import date

from django.db import models
from django.utils.text import slugify
from dateutil.relativedelta import relativedelta

from locations.models import Area


class Bird(models.Model):
    """ Basic bird information """
    class SexChoices(models.TextChoices):
        UNKNOWN = '', 'Unsure/Unknown'
        FEMALE = 'female'
        MALE = 'male'

    class LifeStageChoices(models.TextChoices):
        UNDETERMINED = '', 'Undetermined'
        FLEDGLING = 'fledgling'
        JUVENILE = 'juvenile'
        SUB_ADULT = 'sub-adult'
        ADULT = 'adult'

    class StatusChoices(models.TextChoices):
        UNKNOWN = '', 'Unknown'
        ALIVE = 'alive'
        DEAD = 'dead'

    # Identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(
        max_length=100, editable=False, blank=True, null=True
    )

    # Basic details
    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=15,
        blank=True,
        choices=StatusChoices.choices,
        default=StatusChoices.UNKNOWN
    )
    sex = models.CharField(
        max_length=15,
        blank=True,
        choices=SexChoices.choices,
        default=SexChoices.UNKNOWN
    )
    birthday = models.DateField(blank=True, null=True)

    # Associated area
    area = models.ForeignKey(
        Area,
        related_name='birds',
        on_delete=models.PROTECT,
    )

    # Band details
    primary_band = models.CharField(max_length=20)

    # Metadata
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ Generate slug from name """

        self.slug = slugify(self.name)
        super(Bird, self).save(*args, **kwargs)

    def get_age(self):
        """ Calculates age (in years) based on birthday """

        if (self.status == 'dead') or (self.birthday == None):
            return None

        return relativedelta(date.today(), self.birthday).years

    def get_life_stage(self):
        """ Calculates life stage based on age (integers) """

        age = self.get_age()

        if age != None:
            if age == 0:  # Under 12 months
                return Bird.LifeStageChoices.FLEDGLING.label
            elif age == 1:
                return Bird.LifeStageChoices.JUVENILE.label
            elif age >= 2 and age < 4:
                return Bird.LifeStageChoices.SUB_ADULT.label
            elif age >= 4:
                return Bird.LifeStageChoices.ADULT.label
        return Bird.LifeStageChoices.UNDETERMINED.label
