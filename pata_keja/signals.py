from django.dispatch import reciever
from django.core.signals import pre_save
from .models import houseDesc, booking

@reciever(pre_save, sender=houseDesc)
def add_points(sender,instance, **kwargs):
    pass
    
    
