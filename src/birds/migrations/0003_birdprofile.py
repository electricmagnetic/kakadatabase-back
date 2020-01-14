# Generated by Django 3.0.2 on 2020-01-14 11:21

import birds.models
from django.db import migrations, models
import django.db.models.deletion
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0002_auto_20200114_2334'),
    ]

    operations = [
        migrations.CreateModel(
            name='BirdProfile',
            fields=[
                ('bird', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='bird_profile', serialize=False, to='birds.Bird')),
                ('is_extended', models.BooleanField(default=True, editable=False)),
                ('is_featured', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('sponsor_name', models.CharField(blank=True, max_length=200, null=True)),
                ('sponsor_website', models.URLField(blank=True, null=True)),
                ('profile_picture', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=birds.models.bird_directory_path)),
                ('profile_picture_ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20)),
                ('profile_picture_attribution', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'ordering': ['bird'],
            },
        ),
    ]