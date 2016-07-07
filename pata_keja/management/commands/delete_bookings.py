from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
import datetime
from pata_keja.models import booking

class Command(BaseCommand):
    help='''deletes booking older than 72hrs'''
    #def handle_noargs(self):
        #for booking in bookings.objects.all():
            #if booking.booked_at < timezone.now() +datetime.timedelta(days=-3)):
				#booking.
                #pass
    def add_arguments(self, parser):
		parser.add_argument('book_id', nargs='+', type=int)

    def handle(self, *args, **options):
		for book_id in options['book_id']:
			try:
				book=booking.objects.get(pk=book_id)
				y=book.booked_at + datetime.timedelta(days=3)
				if y < timezone.now():
					book.valid=False
		    		book.save()
		    		self.stdout.write(self.style.SUCCESS('Successfully invalidate booking "%s"' % booking.id))

			except booking.DoesNotExist:
				raise CommandError('Booking "%s" does not exist' % book_id)
	    
		