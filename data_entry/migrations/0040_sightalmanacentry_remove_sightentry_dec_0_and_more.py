# Generated by Django 4.1.7 on 2023-06-06 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_entry', '0039_alter_meridian_passage_entry_dr_longitude_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SightAlmanacEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sight_number', models.IntegerField(default=1, unique=True)),
                ('dec_0', models.CharField(default='-00 00.0', help_text='-DD MM.M -South +North', max_length=8)),
                ('dec_1', models.CharField(default='-00 00.0', help_text='-DD MM.M -South +North', max_length=8)),
                ('gha_0', models.CharField(default='000 00.0', help_text='DDD MM.M', max_length=8)),
                ('gha_1', models.CharField(default='000 00.0', help_text='DDD MM.M', max_length=8)),
                ('sha', models.CharField(default='000 00.0', help_text='DDD MM.M', max_length=8)),
                ('semi_diameter', models.CharField(default='00.0', help_text='MM.M', max_length=4)),
            ],
        ),
        migrations.RemoveField(
            model_name='sightentry',
            name='dec_0',
        ),
        migrations.RemoveField(
            model_name='sightentry',
            name='dec_1',
        ),
        migrations.RemoveField(
            model_name='sightentry',
            name='gha_0',
        ),
        migrations.RemoveField(
            model_name='sightentry',
            name='gha_1',
        ),
        migrations.RemoveField(
            model_name='sightentry',
            name='semi_diameter',
        ),
        migrations.RemoveField(
            model_name='sightentry',
            name='sha',
        ),
    ]