# Generated by Django 4.2.2 on 2023-06-08 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0005_kid_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='kid',
            name='points_history',
            field=models.IntegerField(default=0),
        ),
    ]
