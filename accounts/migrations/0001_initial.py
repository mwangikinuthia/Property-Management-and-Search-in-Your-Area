# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sex', models.CharField(max_length=6, choices=[(b'Male', b'Male'), (b'Female', b'Female')])),
                ('occupation', models.CharField(max_length=30)),
                ('contanct', models.IntegerField(default=0)),
                ('date_of_birth', models.DateField(help_text=b'YYYY-MM-DD', null=True, verbose_name=b'DOB', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
