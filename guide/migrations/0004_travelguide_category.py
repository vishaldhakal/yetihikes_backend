# Generated by Django 5.1 on 2024-11-07 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0003_remove_travelguide_guide_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelguide',
            name='category',
            field=models.CharField(choices=[('Nepal Travel Info', 'Nepal Travel Info'), ('Trekking Info', 'Trekking Info')], default='Nepal Travel Info', max_length=200),
        ),
    ]
