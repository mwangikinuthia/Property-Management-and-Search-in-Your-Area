'''Manages how forms are displayed, initial data they contain and widgets attributes eg hidden'''
from .models import Comment, houseDesc,houseManager,Plot,booking
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','body',)
        widgets = {
            'name': forms.HiddenInput
        }


class HouseForm(forms.ModelForm):
    class Meta:
        model = houseDesc
        fields= ('house_type','image','image_2','rent_per_month','house_owner',
                 'house_email','house_desc','house_bills','plot','available','tags')
        widgets = {
            'house_owner': forms.HiddenInput,
            'house_email': forms.HiddenInput,
        }


class CaretakerForm(forms.ModelForm):
    class Meta:
        model=houseManager
        fields=('first_name','last_name','surname','contanct','email')


class plotUploadForm(forms.ModelForm):
    class Meta:
        model=Plot
        fields=('name','caretaker','contanct','location','No_of_houses'
                ,'availableHouses','nyumba_kumi_rep','plot_number',
                'water_availabity','location_security')
        widgets = {
            'caretaker': forms.HiddenInput,
        }


class bookingForm(forms.ModelForm):
    class Meta:
        model=booking
        fields=('user_name',)
        widgets = {
            'user_name': forms.HiddenInput,
        }


class houseDeleteForm(forms.ModelForm):
    class Meta:
        model = houseDesc
        fields = []


class houseeditForm(forms.ModelForm):
    class Meta:
        model=houseDesc
        fields=('rent_per_month', 'house_bills','house_booked')



class SearchForm(forms.Form):
    query=forms.CharField()

		



