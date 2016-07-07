'''Signals are a nutshell.Tried to impliment them and got bored'''
from django.dispatch import reciever
from django.core.signals import pre_save
from .models import houseDesc, booking

@reciever(pre_save, sender=hoseDesc)
def add_points(sender,,instance, **kwargs):
    pass
    
    
