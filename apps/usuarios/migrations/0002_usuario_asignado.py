# Generated by Django 4.2 on 2023-04-05 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='asignado',
            field=models.BooleanField(default=False),
        ),
    ]
