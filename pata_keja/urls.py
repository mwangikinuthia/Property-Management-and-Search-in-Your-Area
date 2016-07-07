from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
	#house_views
    #url(r'^$', views.houselistView.as_view(), name='house_list'),
    url(r'^$', views.house_list, name='house_list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.house_list, name='house_list_by_tag'),
    url(r'^house/(?P<house_id>\d+)/$',"pata_keja.views.house_detail", name="pata"),
    url(r'^add/$',views.add_house,name="add_house"),
	url(r'^caretakers/$', views.house_caretaker.as_view(), name='caretakers'),
	url(r'^caretakers/add/$',views.add_caretaker, name="caretaker_add"),
    #url(r'^caretakers/panel/$',views.caretaker_panel, name="caretaker_panel"),
    url(r'^caretakers/add-plot/$',views.add_plot, name="add_plot"),
    url(r'^book/(?P<house_id>\d+)/$',views.book,name="book"),
    #url(r'^booking-list$', views.bookinglist, name='booking_list'),
    url(r'^mine$', views.your_house_list, name='mine'),
    url(r'^delete/(?P<house_id>\d+)/$',views.delete_h,name="delete"),
    url(r'^update/(?P<pk>\d+)/$',views.HouseUpdateView.as_view(), name="update"),
    url(r'^my-plots/$', views.your_plot_list, name='my-plots'),
    url(r'^booking-list/$', views.your_bookings, name='booking_list'),
	url(r'^plot-detail/(?P<pk>\d+)/$', views.plot_details, name='plot-detail'),
    url(r'^cancel-booking/(?P<pk>\d+)/$',views.bookingDelete.as_view(), name='cancel-booking'),
    url(r'^search/$', views.house_search, name='house_search'),
    url(r'^mybookings/$',views.myhouseBookings, name='my-bookings'),
    url(r'^approve-booking/(?P<book_id>\d+)/$',views.approveBooking, name='approve-booking'),
]
