# Generated by Django 3.2.8 on 2021-10-06 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='', verbose_name='Name')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='Price')),
                ('available', models.BooleanField(default=True, verbose_name='Is available now?')),
                ('visible', models.BooleanField(default=True, verbose_name='Can be showed on menu?')),
                ('type1', models.TextField(default='', verbose_name='Starter/main/Desert...?')),
                ('index', models.PositiveIntegerField(default=0, verbose_name='Number on the menu (optional)')),
            ],
        ),
    ]