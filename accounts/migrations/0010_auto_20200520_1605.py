# Generated by Django 3.0.6 on 2020-05-20 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200520_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='card_number',
            field=models.CharField(default='1530420010', max_length=10),
        ),
    ]