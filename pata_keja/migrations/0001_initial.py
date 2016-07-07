# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=30)),
                ('booked_at', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('valid', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('body', models.CharField(max_length=140, verbose_name=b'comment')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='houseDesc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(help_text=b'Upload a photo of the house', upload_to=b'photos/%Y/%m/%d')),
                ('image_2', models.ImageField(upload_to=b'photos/%Y/%m/%d', blank=True)),
                ('house_type', models.CharField(max_length=20, choices=[(b'Single room', b'Single room'), (b'Bedsitter', b'Bedsitter'), (b'Double', b'Double'), (b'One bedroom', b'One bedroom'), (b'Two Bedroom', b'Two bedroom'), (b'Three Bedroom', b'Three bedroom')])),
                ('house_owner', models.CharField(max_length=25)),
                ('house_email', models.EmailField(max_length=254)),
                ('rent_per_month', models.IntegerField()),
                ('house_bills', models.CharField(help_text=b'Tenant pays this bills', max_length=30, verbose_name=b'House bills', choices=[(b'Water and Electricity', b'Water and Electricity'), (b'Water only', b'Water only'), (b'Electricity only', b'Electricity only'), (b'Nothing', b'Nothing')])),
                ('house_desc', models.TextField(null=True, verbose_name=b'Description', blank=True)),
                ('total_bookings', models.PositiveIntegerField(default=0, db_index=True)),
                ('slug', models.SlugField(unique_for_date=b'created', blank=True)),
                ('available', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default=b'approved', max_length=15, choices=[(b'not approved', b'Not Approved'), (b'approved', b'Approved')])),
                ('house_booked', models.BooleanField(default=False, verbose_name=b'Booked')),
                ('points', models.IntegerField(default=0, db_index=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='houseManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=10)),
                ('last_name', models.CharField(max_length=10)),
                ('surname', models.CharField(max_length=10, blank=True)),
                ('contanct', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('registered', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default=b'not approved', max_length=15, choices=[(b'not approved', b'Not Approved'), (b'approved', b'Approved')])),
            ],
        ),
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name=b'Plot Name')),
                ('location', models.CharField(help_text=b'Enter nearest town,shopping center or current estate', max_length=40, verbose_name=b'Location')),
                ('location_security', models.CharField(help_text=b'How would you rate the security', max_length=20, verbose_name=b'Security', choices=[(b'Very safe', b'Very safe'), (b'Safe', b'Safe'), (b'Good', b'Good'), (b'Worrying', b'Worrying')])),
                ('plot_number', models.CharField(help_text=b'Enter unique number number', max_length=50, verbose_name=b'Plot Number')),
                ('water_availabity', models.CharField(help_text=b'Water availability', max_length=25, verbose_name=b'water', choices=[(b'More than 5 days PW', b'More than 5 days PW'), (b'Thrice Per week', b'Thrice Per week'), (b'Once Per week', b'Once Per Week'), (b'Not Available', b'N/A')])),
                ('caretaker', models.CharField(max_length=30)),
                ('nyumba_kumi_rep', models.IntegerField(help_text=b'Contact to a trusted tenant')),
                ('availableHouses', models.IntegerField(help_text=b'Current unoccupied houses', verbose_name=b'Availabe houses')),
                ('points', models.IntegerField(default=10, db_index=True)),
                ('contanct', models.IntegerField(verbose_name=b'contact')),
                ('registered', models.DateTimeField(auto_now_add=True)),
                ('No_of_houses', models.IntegerField(help_text=b'number of all houses', verbose_name=b'Total houses')),
                ('status', models.CharField(default=b'approved', max_length=15, choices=[(b'not approved', b'Not Approved'), (b'approved', b'Approved')])),
                ('updated', models.DateTimeField(auto_now=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
        ),
        migrations.AddField(
            model_name='housedesc',
            name='plot',
            field=models.ForeignKey(related_name='house', to='pata_keja.Plot'),
        ),
        migrations.AddField(
            model_name='housedesc',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text=b'Enter house location and type.\nie kariobangi, bedsitter', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(related_name='comment', to='pata_keja.houseDesc'),
        ),
        migrations.AddField(
            model_name='booking',
            name='house_booked',
            field=models.ForeignKey(related_name='booking', to='pata_keja.houseDesc'),
        ),
    ]
