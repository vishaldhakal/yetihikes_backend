# Generated by Django 5.1 on 2024-11-07 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0021_activity_youtube_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='itineraryactivity',
            name='accomodation',
            field=models.TextField(blank=True),
        ),
    ]
