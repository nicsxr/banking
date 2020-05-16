# Generated by Django 3.0.6 on 2020-05-16 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200512_0012'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=30)),
                ('receiver', models.CharField(max_length=30)),
                ('sentMoney', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='account',
            name='card_number',
            field=models.CharField(default='7718372466', max_length=10),
        ),
    ]
