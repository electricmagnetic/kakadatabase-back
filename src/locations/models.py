import uuid

from django.contrib.gis.db import models
from django.utils.text import slugify


class Area(models.Model):
    """ Basic location information """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Place(models.Model):
    """ Place used to generate geocode strings """

    name_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    feat_type = models.CharField(max_length=200, blank=True, null=True)
    land_district = models.CharField(max_length=200, blank=True, null=True)

    point = models.PointField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Region(models.Model):
    """ Wider regions, designed to be made up of Area objects """

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, primary_key=True, editable=False)

    description = models.CharField(max_length=200, blank=True, null=True)

    areas = models.ManyToManyField(Area)

    polygon = models.MultiPolygonField(null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ Generate slug from name """

        self.slug = slugify(self.name)
        super(Region, self).save(*args, **kwargs)
