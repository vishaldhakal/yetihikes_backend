# Generated by Django 5.1 on 2025-01-05 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0026_activitytestimonial_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='meta_keywords',
            field=models.TextField(blank=True),
        ),
    ]
