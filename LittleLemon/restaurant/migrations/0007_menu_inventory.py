# Generated by Django 4.2 on 2023-07-21 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_alter_menu_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='inventory',
            field=models.IntegerField(default=1),
        ),
    ]
