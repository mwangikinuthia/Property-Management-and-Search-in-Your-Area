from django.db import models
from django.conf import settings

# Creates a Profile model which inherits most attr from AUTH_USER_MODEL.
class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL)#creates onetoone  relationship with the user model
    sex=models.CharField(max_length=6,choices=(('Male','Male'),('Female','Female'),))
    occupation=models.CharField(max_length=30)
    contanct=models.IntegerField(default=0)
    date_of_birth=models.DateField("DOB",help_text="YYYY-MM-DD",blank=True,null=True)
    def __unicode__(self):
        return '{} Profile'.format(self.user.username)
    
