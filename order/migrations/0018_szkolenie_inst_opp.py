# Generated by Django 4.1.1 on 2022-11-07 23:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_szkolenie_opp'),
    ]

    operations = [
        migrations.CreateModel(
            name='szkolenie_inst_opp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imie', models.CharField(max_length=20)),
                ('nazwisko', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('nazwa_firmy', models.CharField(max_length=100)),
                ('numer_nip', models.CharField(max_length=10)),
                ('numer_telefonu', models.CharField(max_length=11)),
                ('data', models.DateField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]