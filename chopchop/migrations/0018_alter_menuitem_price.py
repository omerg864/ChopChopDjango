# Generated by Django 3.2.8 on 2022-02-08 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chopchop', '0017_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='price',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=19, verbose_name='Price'),
        ),
    ]