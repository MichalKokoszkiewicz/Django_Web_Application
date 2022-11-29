# Generated by Django 4.1.1 on 2022-11-07 23:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_szkolenie_inst_opp'),
    ]

    operations = [
        migrations.CreateModel(
            name='audyt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rodzaj_audytu', models.CharField(choices=[('Przeciwpożarowy', 'Przeciwpożarowy'), ('BHP', 'BHP')], max_length=50)),
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
