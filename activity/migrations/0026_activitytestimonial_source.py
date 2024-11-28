# Generated by Django 5.1 on 2024-11-28 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0025_cupon_valid_from_cupon_valid_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitytestimonial',
            name='source',
            field=models.CharField(blank=True, choices=[('Trip Advisor', 'Trip Advisor'), ('Trust Pilot', 'Trust Pilot'), ('Google', 'Google'), ('Others', 'Others')], default='Others', max_length=500),
        ),
    ]
