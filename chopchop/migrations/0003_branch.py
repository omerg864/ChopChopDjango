# Generated by Django 3.2.8 on 2021-10-06 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chopchop', '0002_auto_20211007_0026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='', verbose_name='Branch name')),
                ('slug', models.SlugField(null=True)),
            ],
        ),
    ]
