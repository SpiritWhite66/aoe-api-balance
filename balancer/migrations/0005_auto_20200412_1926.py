# Generated by Django 3.0.5 on 2020-04-12 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balancer', '0004_auto_20200411_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='rating',
            field=models.IntegerField(default=1000),
        ),
    ]