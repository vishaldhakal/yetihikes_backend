# Generated by Django 5.1 on 2025-01-05 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0029_alter_activitybooking_arrival_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='departuredate',
            name='max_seats',
            field=models.IntegerField(default=0),
        ),
    ]
