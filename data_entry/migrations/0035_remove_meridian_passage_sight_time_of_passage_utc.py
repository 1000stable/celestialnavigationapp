# Generated by Django 4.1.7 on 2023-05-01 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_entry', '0034_alter_meridian_passage_sight_eye_height_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meridian_passage_sight',
            name='time_of_passage_utc',
        ),
    ]
