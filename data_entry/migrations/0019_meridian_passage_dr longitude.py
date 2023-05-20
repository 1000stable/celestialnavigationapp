# Generated by Django 4.1.7 on 2023-04-11 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_entry', '0018_meridian_passage_sight_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='meridian_passage',
            name='DR Longitude',
            field=models.CharField(default='000 00.0E', help_text='DDD MM.MX where X is either W(est) or E(ast)', max_length=9, null=True),
        ),
    ]
