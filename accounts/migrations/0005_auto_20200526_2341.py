# Generated by Django 3.0.6 on 2020-05-26 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200526_2337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='number1',
        ),
        migrations.AddField(
            model_name='card',
            name='number',
            field=models.CharField(default='2509665676', max_length=10),
        ),
        migrations.AlterField(
            model_name='account',
            name='card_number',
            field=models.CharField(default='9765731166', max_length=10),
        ),
    ]
