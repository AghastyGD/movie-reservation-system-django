# Generated by Django 5.1 on 2024-09-01 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0005_showtime_num_seats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showtime',
            name='num_seats',
            field=models.PositiveIntegerField(default=50),
        ),
    ]
