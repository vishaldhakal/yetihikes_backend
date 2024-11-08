# Generated by Django 5.1 on 2024-11-08 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0004_travelguide_category'),
        ('home', '0013_newslettersubscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuideDropdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guides', models.ManyToManyField(blank=True, to='guide.travelguide')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
