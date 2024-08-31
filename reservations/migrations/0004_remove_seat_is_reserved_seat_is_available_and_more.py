# Generated by Django 5.1 on 2024-08-31 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_seat_reservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seat',
            name='is_reserved',
        ),
        migrations.AddField(
            model_name='seat',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='seat',
            name='seat_number',
            field=models.CharField(max_length=10),
        ),
    ]
