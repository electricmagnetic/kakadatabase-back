# Generated by Django 3.0.2 on 2020-01-16 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0005_auto_20200115_0359'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bird',
            options={'ordering': ['name', 'primary_band']},
        ),
    ]
