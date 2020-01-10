# Generated by Django 3.0.2 on 2020-01-10 13:22

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('name_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('feat_type', models.CharField(blank=True, max_length=200, null=True)),
                ('land_district', models.CharField(blank=True, max_length=200, null=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('polygon', django.contrib.gis.db.models.fields.PolygonField(null=True, srid=4326)),
                ('areas', models.ManyToManyField(to='locations.Area')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
