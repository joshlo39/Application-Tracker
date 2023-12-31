# Generated by Django 4.2.7 on 2023-11-16 00:03

import datetime
import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='internship',
            name='city',
            field=models.CharField(default='Tallahassee', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='internship',
            name='state',
            field=models.CharField(default='Florida', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='internship',
            name='date_posted',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(default='UserAbstract', error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
            preserve_default=False,
        ),
    ]
