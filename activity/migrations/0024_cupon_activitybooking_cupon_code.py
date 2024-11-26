# Generated by Django 5.1 on 2024-11-26 11:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0023_activity_related_activities_activity_related_blogs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('discount', models.FloatField()),
                ('active', models.BooleanField(default=True)),
                ('activities', models.ManyToManyField(blank=True, to='activity.activity')),
            ],
        ),
        migrations.AddField(
            model_name='activitybooking',
            name='cupon_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='activity.cupon'),
        ),
    ]
