# Generated by Django 4.1.7 on 2023-04-30 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_entry', '0032_rename_presure_meridian_passage_sight_pressure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meridian_passage_sight',
            name='index_error',
            field=models.CharField(default='00.0', help_text='+MM.M + = off arc, - = on arc', max_length=5),
        ),
    ]
