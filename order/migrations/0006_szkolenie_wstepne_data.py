# Generated by Django 4.1.1 on 2022-11-05 18:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_remove_szkolenie_wstepne_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='szkolenie_wstepne',
            name='data',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
