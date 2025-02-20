# Generated by Django 5.1 on 2025-02-10 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0030_departuredate_max_seats'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='best_season',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='difficulty_level',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='group_style',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='max_altitude',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='trip_start',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='trips_end',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
