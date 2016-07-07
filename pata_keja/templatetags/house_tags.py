from django import template
from django.db.models  import Count
from django.contrib.auth.models import Group
from ..models import houseDesc, booking,Plot
register=template.Library()

@register.inclusion_tag('house/detail.html')
def top_houses(houseDesc):
	top_h= houseDesc.approved.all().order_by('-points')
	return {'top_h':top_h}
@register.simple_tag()
def total_houses():
	return houseDesc.approved.count()
@register.simple_tag(takes_context=True)
def house_points(context, house_id):
	house=houseDesc.objects.get(pk=house_id)
	b=house.booking.count()*5
	if house.comment.count() <= 10:
		cp=3
	else:
		cp=5
	points=cp+b
	return points
@register.simple_tag()
def decrement_id(user_id):
	return user_id-1
#@register.inclusion_tag('pata_keja/base.html')
#def top_houses(count = 3):
	#top_5=houseDesc.objects.order_by('points')[:count]
	#return { 'top_5':top_5 ,}


#buggy
@register.inclusion_tag('pata_keja/house/latest_houses.html')
def show_latest_houses(count=3):
	latest_houses=houseDesc.approved.order_by('-created')[:count]
	return {'latest_houses':latest_houses,}
@register.filter(name='member_of')
def member_of(user, group_name):
	group=Group.objects.get(name=group_name)
	return True if group in user.groups.all() else False
@register.inclusion_tag('pata_keja/dash.html')
def no_of_your_houses(request):
	v=houseDesc.objects.filter(house_owner__startswith=request.user.username).count()
	return {'v':v}
@register.filter(name='profile_id')
def profile_id(house_id):
	house_=houseDesc.objects.get(id=house_id)
	y=house_.bookings.values()
	p_ids=[]
	for dic in y:
		user_=dic.pop('user_name')
		y_=user_.profile.id
		p_ids.append(y_)
	return p_ids
@register.assignment_tag
def trending(count=3):
	return houseDesc.approved.annotate(total_points=Count('points')).order_by('-points')[:count]
@register.inclusion_tag('pata_keja/dash.html')
def top_places():
	x= Plot.objects.order_by('points')
	return {'x':x}	
	
@register.simple_tag(takes_context=True)	
def no_of_your_bookings(context):
	user_=context['user']
	return booking.objects.filter(user_name__startswith=user_).count()
@register.assignment_tag
def top_plots(count=3):
	return Plot.approved.annotate(total_points=Count('points')).order_by('-points')[:count]
	
def approve(request, book_id):
	book=booking.validated.get(pk=book_id)
	house=book.house_booked
	house.available=False
	book.approved=True
	plot=house.plot
	plot.availableHouses=plot.availableHouses-1