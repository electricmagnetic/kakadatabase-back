import uuid
from datetime import date

from django.db import models
from django.utils.text import slugify
from django.dispatch import receiver
from versatileimagefield.fields import VersatileImageField, PPOIField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer
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
        max_length=50, editable=False, blank=True, null=True
    )

    # Basic details
    name = models.CharField(max_length=30, null=True, blank=True)
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
        return self.get_label()

    def save(self, *args, **kwargs):
        """ Generate slug from name """

        if self.name:
            self.slug = slugify(self.name)
        else:
            self.slug = None
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

    def get_label(self):
        """ Creates a label for the bird from either a name or a band """
        return self.name or self.primary_band


def bird_directory_path(instance, filename):
    """ Helper function for determining upload location for BirdProfile """
    return 'birds/%s/%s' % (instance.bird.id, filename)


class BirdProfile(models.Model):
    """ Bird profile information """
    bird = models.OneToOneField(
        Bird,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile'
    )

    # Metadata
    is_extended = models.BooleanField(default=True, editable=False)

    # Details
    is_featured = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    sponsor_name = models.CharField(max_length=200, null=True, blank=True)
    sponsor_website = models.URLField(max_length=200, null=True, blank=True)

    # Image
    picture = VersatileImageField(
        upload_to=bird_directory_path,
        blank=True,
        null=True,
        ppoi_field='picture_ppoi'
    )
    picture_ppoi = PPOIField()
    picture_attribution = models.CharField(
        max_length=200, null=True, blank=True
    )

    class Meta:
        ordering = [
            'bird',
        ]

    def __str__(self):
        return str(self.bird)


@receiver(models.signals.post_save, sender=BirdProfile)
def warm_BirdProfile_pictures(sender, instance, **kwargs):
    """Ensures BirdProfile thumbnails are created post-save"""
    picture_warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set='profile_picture',
        image_attr='picture'
    )
    num_created, failed_to_create = picture_warmer.warm()
