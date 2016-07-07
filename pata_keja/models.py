from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
# Creates models  which are tables in the database
# Managers are object managers for retrieving items from the db

#gets approved houses and plots


class ApprovedManager(models.Manager):
	def get_queryset(self):
		return super(ApprovedManager,self).get_queryset().filter(status='approved')


class AvailableManager(models.Manager):
	def get_queryset(self):
		return super(AvailableManager,self).get_queryset().filter(available=True)
#how a house/property is stored at the db
class houseDesc(models.Model):
	STATUS_CHOICES=(
	('not approved', 'Not Approved'),
	('approved', 'Approved'),)    
	HOUSE_TYPE_CHOICES=(
	        ('Single room','Single room'),
	        ('Bedsitter', 'Bedsitter'), 
	        ('Double','Double'),
	        ('One bedroom', 'One bedroom'),
	        ('Two Bedroom', 'Two bedroom'),
	        ('Three Bedroom', 'Three bedroom'),
	) 
	
	Owner_pays=(
	        ('Water and Electricity','Water and Electricity'),
	        ('Water only','Water only'),
	        ('Electricity only','Electricity only'),
	        ('Nothing','Nothing'),
	)
	
	plot=models.ForeignKey("Plot",related_name='house')
	image=models.ImageField(upload_to='photos/%Y/%m/%d',help_text="Upload a photo of the house")
	image_2=models.ImageField(upload_to='photos/%Y/%m/%d',blank=True)
	house_type=models.CharField(max_length=20, choices=HOUSE_TYPE_CHOICES)
	house_owner=models.CharField(max_length=25)
	house_email=models.EmailField()
	rent_per_month=models.IntegerField()
	house_bills=models.CharField("House bills",max_length=30,choices=Owner_pays,help_text="Tenant pays this bills")
	house_desc=models.TextField("Description", blank=True,null=True)
	total_bookings=models.PositiveIntegerField(db_index=True, default=0)
	slug=models.SlugField(max_length=50,unique_for_date='created', blank=True)
	available=models.BooleanField(default=True)
	
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)
	status=models.CharField(max_length=15,choices=STATUS_CHOICES,default='approved')
	house_booked=models.BooleanField("Booked",default=False)
	points=models.IntegerField(default=0,db_index=True)
	objects =models.Manager()
	house_available=AvailableManager()
	approved=ApprovedManager()
	tags=TaggableManager(help_text="Enter house location and type.\nie kariobangi, bedsitter")
	
	
	class Meta:
		ordering=('-created',)	
			
	def __unicode__(self):
		return self.house_type+' in '+self.plot.name+' '+str(self.id)
	
class Comment(models.Model):
	post = models.ForeignKey(houseDesc, related_name='comment')#comment depends on a house.a comment can velong to a single house
	name = models.CharField(max_length=80)
	body = models.CharField("comment",max_length=140)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)#we display active comments so we can mute a rude or improper comment to active=False
	
	class Meta:
		ordering = ('created',)
	
	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.post)
	
	
	
class houseManager(models.Model):
	STATUS_CHOICES=(
	        ('not approved', 'Not Approved'),
		('approved', 'Approved'),)	
	first_name=models.CharField(max_length=10)
	last_name=models.CharField(max_length=10)
	surname=models.CharField(max_length=10, blank=True)
	contanct=models.IntegerField()
	email=models.EmailField()
	registered=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)	
	status=models.CharField(max_length=15,choices=STATUS_CHOICES,default='not approved')
	approved=ApprovedManager()
	def __unicode__(self):
			return self.first_name+' '+self.last_name	
class Plot(models.Model):
	STATUS_CHOICES=(
	        ('not approved', 'Not Approved'),
		('approved', 'Approved'),)
	Security_choices=(
		        ( 'Very safe','Very safe'),
		        ( 'Safe','Safe'),
		        ( 'Good', 'Good'),
		        ( 'Worrying','Worrying'),
		)
	tap_water_availability=(
	        ('More than 5 days PW','More than 5 days PW'),
	        ('Thrice Per week','Thrice Per week'),
	        ('Once Per week','Once Per Week'),
	        ('Not Available', 'N/A'),
	)
	name=models.CharField("Plot Name",max_length=30)
	location=models.CharField("Location",max_length=40,help_text="Enter nearest town,shopping center or current estate")
	location_security=models.CharField("Security",help_text="How would you rate the security",max_length=20, choices=Security_choices)
	plot_number=models.CharField("Plot Number",max_length=50,help_text="Enter unique number number")
	water_availabity=models.CharField("water",help_text="Water availability",choices=tap_water_availability,max_length=25)
	caretaker=models.CharField(max_length=30)
	nyumba_kumi_rep=models.IntegerField(help_text="Contact to a trusted tenant")
	availableHouses=models.IntegerField("Availabe houses",help_text="Current unoccupied houses")
	points=models.IntegerField(default=10,db_index=True)
	contanct=models.IntegerField("contact")
	registered=models.DateTimeField(auto_now_add=True)
	No_of_houses=models.IntegerField("Total houses",help_text="number of all houses")
	status=models.CharField(max_length=15,choices=STATUS_CHOICES,default='approved')
	updated=models.DateTimeField(auto_now=True)
	tags=TaggableManager()
	approved=ApprovedManager()
	objects =models.Manager()
	
	def __unicode__(self):
		return self.name
class bookapprovedManager(models.Manager):
	def get_queryset(self):
		return super(bookapprovedManager, self).get_queryset().filter(approved=True)
class bookingValidManager(models.Manager):
	def get_queryset(self):
		return super(bookingValidManager, self).get_queryset().filter(valid=True)
class booking(models.Model):
	user_name=models.CharField(max_length=30)
	house_booked=models.ForeignKey(houseDesc, related_name='booking')
	booked_at=models.DateTimeField(auto_now_add=True,editable=False)
	approved=models.BooleanField(default=False)
	valid=models.BooleanField(default=True)
	objects=models.Manager()
	bookapproved=bookapprovedManager()
	validated=bookingValidManager()
	def __unicode__(self):
		return self.user_name

