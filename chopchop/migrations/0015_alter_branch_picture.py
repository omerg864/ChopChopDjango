# Generated by Django 3.2.8 on 2021-10-07 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chopchop', '0014_auto_20211007_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='picture',
            field=models.TextField(blank=True, default='', verbose_name='Picture Url'),
        ),
    ]
