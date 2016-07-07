from django.shortcuts import render,get_object_or_404,render_to_response
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView
from .models import houseDesc, Comment,houseManager,Plot,booking
from .rank import house_points,house_ranking,plot_rank,plot_rating
from .forms import CommentForm, HouseForm,CaretakerForm,plotUploadForm,bookingForm,houseDeleteForm,houseeditForm,SearchForm
from taggit.models import Tag
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from accounts.models import Profile
from haystack.query import SearchQuerySet
from django.db.models import Count

#my views are all here
#returns a list of all houses/properties with pagination


def landing_view(request):
    return render(request, 'pata_keja/landing.html', {})


def house_list(request, tag_slug=None):
    top_5 = houseDesc.objects.order_by('-points')[5:]
   
    house_list = houseDesc.house_available.all()
    tag = None
    y= Plot.objects.order_by('points')[:1]
    x=y.reverse()
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        house_list = house_list.filter(tags__in=[tag])

    paginator = Paginator(house_list, 3) # 3 houses in each page
    page = request.GET.get('page')
    try:
        houses = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        houses = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        houses = paginator.page(paginator.num_pages)
    return render(request, 'pata_keja/house/list.html', {'page': page,
                                                   'houses': houses,
                                                   'tag': tag,
                                                   'x':x,
                                                   'top_5':top_5,
                                                   })
#@login_requred decorator ensures any who tries to view here must be logged in
#user_passes_test ensure the user is  a member of the caretakers group which have it special permissions
@login_required
@user_passes_test(lambda u: u.groups.filter(name='caretakers'))
def your_house_list(request, tag_slug=None):
    v=houseDesc.objects.filter(house_owner__startswith=request.user.username).count()
    house_list = houseDesc.objects.filter(house_owner=request.user.username)
    house_num = houseDesc.objects.filter(house_owner=request.user.username).count()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        house_list = house_list.filter(tags__in=[tag])

    paginator = Paginator(house_list, 3) # 3 houses in each page
    page = request.GET.get('page')
    try:
        houses = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        houses = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        houses = paginator.page(paginator.num_pages)
    return render(request, 'pata_keja/house/your_houses.html', {'page': page,
                                                   'houses': houses,
                                                   'tag': tag,
                                                   'house_num':house_num,
                                                   'v':v})

#@login_requred decorator ensures any who tries to view here must be logged in
#user_passes_test ensure the user is  a member of the caretakers group which have it special permissions
@login_required
@user_passes_test(lambda u: u.groups.filter(name='caretakers'))
def your_plot_list(request):
    v=Plot.approved.filter(caretaker__startswith=request.user.username).count()
    
    plot_list = Plot.approved.filter(caretaker__startswith=request.user.username)
    plot_num = Plot.approved.filter(caretaker__startswith=request.user.username).count()
    paginator = Paginator(plot_list, 4)
    page = request.GET.get('page')
    try:
        plots = paginator.page(page)
    except PageNotAnInteger:
        plots = paginator.page(1)
    except EmptyPage:
        plots = paginator.page(paginator.num_pages)
    return render(request, 'pata_keja/house/plot_list.html', {'page': page,
	                                               'plots': plots,
	                                               'plot_num':plot_num,
                                                       #'no_of_houses':no_of_houses,
	                                               'v':v})    
     
    
#Displays the house

def house_detail(request,house_id=1):
    house=get_object_or_404(houseDesc,pk=house_id)
    plot_id=house.plot.id
    plot_=Plot.approved.all().filter(id=plot_id)
    details=plot_[0]
    bookings=house.booking.count()
    bookers=house.booking.values()
    z=[str(i.get('user_name')) for i in bookers]
    
    #used display bookers profiles for the caretakers to view
    def a_(z):
        profiles=[]
        for i in range(len(z)):
            try:
                p=profiles.append(User.objects.get(username=z[i]))
            except Exception:
                pass
        return profiles
    p=a_(z)
    
    top_5=houseDesc.objects.order_by('-points')[5:]
    comments = house.comment.filter(active=True)
    house_tags_ids=house.tags.values_list('id',flat=True)
    similar_houses=houseDesc.approved.filter(tags__in=house_tags_ids)\
        .exclude(id=house.id)
    similar_houses=similar_houses.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags', '-created')[:4]                                                                        
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            name=comment_form.cleaned_data['name']
            body=comment_form.cleaned_data['body']
            post_id=house_id#assign the comment to tke house
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post_id = post_id#assign the comment to tke house
            # Save the comment to the database
            new_comment.save()
	    
            return HttpResponseRedirect('/patakeja/house/{}/'.format(house_id))
    else:
        comment_form = CommentForm(initial={'name':request.user.username})
        #booking_form =bookingForm()
    return render(request, 'pata_keja/house/detail.html',
                  {'comment_form':comment_form,
                   'house':house,
                   'bookings':bookings,
                   'bookers':bookers,
                   'comments': comments,
                   'details':details,
                   'z':z,
                   'top_5':top_5,
                   'p':p,
                   'similar_houses':similar_houses,
                   #'p_ids':p_ids
                   })
#@login_requred decorator ensures any who tries to view here must be logged in
#user_passes_test ensure the user is  a member of the caretakers group which have it special permissions
@login_required
@user_passes_test(lambda u: u.groups.filter(name='caretakers'))
def add_house(request):
    messages.info(request, "Before adding a house please ensure you have registerd the plot/estate")
    if request.method =='POST':
        house_form=HouseForm(request.POST, request.FILES)
        if house_form.is_valid():
            house_form.save(commit=False)
            house_form.save()
            house_ranking()
            #messages.success(request, "House added succesfully")
            return HttpResponseRedirect('/patakeja')
    else:
        house_form = HouseForm(initial={'house_owner':request.user.username,'house_email':request.user.email})
    return render(request,'pata_keja/house/house_form.html', {'house_form':house_form})


class house_caretaker(ListView):
    queryset=houseManager.approved.all()
    context_object_name='caretakers'
    paginate_by=10
    template_name="pata_keja/house/caretakers_list.html"


def house_caretaker_detail(request, caretaker_id=1):
    caretaker=get_object_or_404(houseManager, pk =caretaker_id)
    return render(request, 'pata_keja/house/caretaker.html', {"caretaker":caretaker})

def add_caretaker(request):
    if request.method =='POST':
        caretaker_form=CaretakerForm(data=request.POST)
        if caretaker_form.is_valid():
            caretaker_form.save()
            return HttpResponseRedirect('/patakeja/caretataker/')
        else:
            caretaker_form=CaretakerForm()
            return render(request, 'pata_keja/house/caretaker_form.html', {'caretaker_form':caretaker_form})
#@login_requred decorator ensures any who tries to view here must be logged in
#user_passes_test ensure the user is  a member of the caretakers group which have it special permissions

@login_required
@user_passes_test(lambda u: u.groups.filter(name='caretakers'))  
def add_plot(request):
    if request.method =='POST':
        plot_form=plotUploadForm(data=request.POST)
        if plot_form.is_valid():
            plot_form.save()
            plot_rating()
            return HttpResponseRedirect('/patakeja/')
    else:
        plot_form=plotUploadForm(initial={'caretaker':request.user.username})
    return render(request, 'pata_keja/house/plot.html',{'plot_form':plot_form})
#@login_requred decorator ensures any who tries to view here must be logged in
#user_passes_test ensure the user is  a member of the tenant group which have it special permissions

@login_required
@user_passes_test(lambda u: u.groups.filter(name='tenant'))   
def book(request, house_id=1):
    #uses sessions so as the user cant book more the once
    if request.session.get('has_booked', False):
        messages.info(request, "You have arledy booked")
        return HttpResponseRedirect('/patakeja/house/{}/'.format(house_id))
    house=get_object_or_404(houseDesc,pk=house_id)
    
    bookings=house.booking.count()
    x=request.user.username
    booker=User.objects.get(username=x)
    booker_profile=Profile.objects.get(pk=booker.profile.id)
    if request.method =='POST':
        booking_form=bookingForm(data=request.POST)
        if booking_form.is_valid():
            username=request.user.username
            time_=timezone.now()
            #need aphone_no
            Email=request.user.email
            phone_no=booker_profile.contanct
            plot=house.plot
            to=house.house_email
            subject='House booked'
            message='A house at {} was booked by {} on {}.\nYou can contanct the booker through Email {}' \
                    '\nPhone number is 0{}'.format(plot, username,time_,Email,phone_no)
            house_booked_id=house_id
            new_booking=booking_form.save(commit=False)
            new_booking.house_booked_id=house_booked_id
            house.booking.create(user_name=booker,booked_at=time_)
            house.house_booked=True
            house.save()
            request.session['has_booked'] = True
            #Sends email to the property owner with bookers detail
            send_mail(subject, message, 'admin@patakeja.com',[to])
            messages.info(request, "An email will be sent to the caretaker to notify him about your booking")
            return HttpResponseRedirect('/patakeja/house/{}/'.format(house_id))
    else:
        messages.info(request, "please update profile with latest info before booking")
        booking_form=bookingForm(initial={'user_name':request.user.username})
    return render(request, 'pata_keja/house/book.html',{'booking_form':booking_form,'booker':booker})
    
    

#@login_requred decorator ensures any who tries to view here must be logged in
#user_passes_test ensure the user is  a member of the caretakers group which have it special permissions
@login_required
@user_passes_test(lambda u: u.groups.filter(name='caretakers'))
def delete_h(request, house_id):
    delete_house = get_object_or_404(houseDesc, pk=house_id)
    if request.method:
        form = houseDeleteForm(request.POST, instance=delete_house)
        if form.is_valid():
            # checks CSRF
            delete_house.delete()
            return HttpResponseRedirect("/patakeja/mine") # wherever to go after deleting
        else:
            form = houseDeleteForm(instance=delete_house)
            template_vars = {'form': form}
            return render(request, 'pata_keja/house/list.html', template_vars)


class HouseUpdateView(UpdateView):
    model =houseDesc
    fields=['rent_per_month','house_bills','image','available']
    template_name_suffix='_update_form'
    
    def get_success_url(self):
        return reverse('pata_keja:mine')


def your_bookings(request):
    you=request.user.username
    bookings=booking.validated.filter(user_name=you)
    return render(request, 'pata_keja/house/booking_list.html',{ 'bookings':bookings })

def plot_details(request, pk=1):
    plot=Plot.objects.get(pk=pk)
    return render(request, 'pata_keja/house/plot_detail.html',{ 'plot':plot })

class bookingDelete(DeleteView):
    model = booking
    success_url = reverse_lazy('pata_keja:house_list')
    
def house_search(request):
    form=SearchForm()
    cd=''
    results=''
    total_results=''
    if 'query' in request.GET:
        global cd
        global results
        global total_results
        form=SearchForm(request.GET)
        if form.is_valid():
            cd=form.cleaned_data
            results=SearchQuerySet().models(houseDesc).filter(content=cd['query']).load_all()
            total_results=results.count()

            return render(request, 'pata_keja/house/search.html',
	                  {'form':form,
	                   'cd':cd,
	                   'results':results,
	                   'total_results':total_results
                           })
    #This view is used to search.As you global keyword is used this is to avoid local unbound error in python2


def plot_search(request):
    form=SearchForm()
    cd=''
    results=''
    total_results=''
    if 'query' in request.GET:
        global cd
        global results
        global total_results
        form=SearchForm(request.GET)
        if form.is_valid():
            cd=form.cleaned_data
            results=SearchQuerySet().models(Plot).filter(content=cd['query']).load_all()
            total_results=results.count()

        return render(request, 'pata_keja/house/search.html',
	                  {'form':form,
	                   'cd':cd,
	                   'results':results,
	                   'total_results':total_results
                           })
#@login_requred decorator ensures any who tries to view here must be logged in
#user_passes_test ensure the user is  a member of the caretakers group which have it special permissions

@login_required
@user_passes_test(lambda u: u.groups.filter(name='caretakers'))
def myhouseBookings(request):
    myHouses=houseDesc.objects.filter(house_owner__startswith=request.user.username)
    allBookings=booking.objects.all()
    myBooking=[]
    approved=[]
    for book in allBookings:
        if book.house_booked in myHouses:
            if book.approved:
                approved.append(book)
            else:
                myBooking.append(book)

    return render(request, 'pata_keja/house/mybookings.html',
		  {'myBooking':myBooking,
                   'approved':approved})

#@login_requred decorator ensures any who tries to view here must be logged in
#user_passes_test ensure the user is  a member of the caretakers group which have it special permissions


@login_required
@user_passes_test(lambda u: u.groups.filter(name='caretakers'))
def approveBooking(request, book_id):
    book=booking.validated.get(pk=book_id)
    book_user=book.user_name
    house=book.house_booked
    house.available=False
    book.approved=True
    plot_=house.plot
    plot=house.plot.name
    plot_filter=Plot.objects.filter(name__startswith=plot)
    x=plot_.availableHouses-1
    plot_filter.update(availableHouses=x)
    house.save()
    plot_.save()
    book.save()
    other_bookings=booking.objects.filter(user_name=book_user).exclude(id=book.id)
    for z in other_bookings:
        z.valid=False
        z.save()
        messages.info(request, "The booking was approved")
    return render(request, 'pata_keja/house/approveBooking.html',
		  {'book':book,
                   'plot':plot,
                   })
