from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, registerForm,caretakerRegisterForm,userEditForm,profileEditForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import Group, User


# Create your views here.
def user_log(request):
    #if you add request.method=='POST' is it a bug i dont know
    if request.method:
        form = LoginForm(request.POST)
        if form.is_valid():
            cleandata = form.cleaned_data
            # Authenticate checks if credentials exists in db
            user=authenticate(username=cleandata['username'],
                              password=cleandata['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/patakeja")
                else:
                    return HttpResponseRedirect("/patakeja")
            else:
                return HttpResponse("Invalid login")
        else:
            form=LoginForm()
        return render(request, 'registration/login.html',{'form':form})
def caretaker_log(request):
    #if you add request.method=='POST'
    if request.method:
        form = LoginForm(request.POST)
        if form.is_valid():
            cleandata=form.cleaned_data
            user=authenticate(username=cleandata['username'],
                              password=cleandata['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/patakeja")
                else:
                    return HttpResponseRedirect("/patakeja")
            else:
                return HttpResponse("Invalid login")
        else:
            form=LoginForm()
        return render(request, 'registration/caretaker_dash.html',{'form':form})
    

@login_required#checks if user is authenticated
def myboard(request):
    return render(request, 'accounts/myboard.html', {'section': 'myboard'})

def register(request):
    if request.method:
        user_form=registerForm(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile=Profile.objects.create(user=new_user)#creates a blank profile
            new_user.groups.add(Group.objects.get(name='tenant'))
            return render(request, 'registration/register_done.html',{'new_user':new_user})
        
        else:
            user_form=registerForm()
        return render(request, 'registration/register.html', {'user_form':user_form})

def registerCaretaker(request):
    if request.method:
        caretaker_form=caretakerRegisterForm(request.POST)
        if caretaker_form.is_valid():
            new_caretaker=caretaker_form.save(commit=False)
            new_caretaker.set_password(caretaker_form.cleaned_data['password'])
	    new_caretaker.is_active=True#This willsoon be off 
            new_caretaker.save()
	    profile=Profile.objects.create(user=new_caretaker)#creates a blank profile
	    new_caretaker.groups.add(Group.objects.get(name='caretakers'))
	    
            
            
            return render(request, 'registration/register_done.html',{'new_caretaker':new_caretaker})
        
        else:
            caretaker_form=caretakerRegisterForm()
        return render(request, 'registration/caretaker_register.html', {'caretaker_form':caretaker_form})

@login_required

def edit(request):
    if request.method=='POST':
	user_form=userEditForm(instance=request.user, data=request.POST)
	profile_form=profileEditForm(instance=request.user.profile, data=request.POST)
	
	if user_form.is_valid and profile_form.is_valid():
	    user_form.save()
	    profile_form.save()
	    messages.success(request, 'Profile updated succesfilly')
	    
	    #return HttpResponseRedirect("")
	else:
	    messages.error(request, 'Error updating profile')
	    
	    
    else:
	user_form=userEditForm(instance=request.user)
	profile_form=profileEditForm(instance=request.user.profile)
    return render(request, 'accounts/edit.html',
		  {'user_form':user_form,
                   'profile_form':profile_form})
@login_required
@user_passes_test(lambda u: u.groups.filter(name='caretakers'),login_url='/patakeja')
def profile_view(request, user_id):
    my_profile=Profile.objects.get(pk=user_id)
    return render(request, 'accounts/profile.html',{'my_profile':my_profile})
def profile_view_2(request, username):
    my_profile=User.objects.get(username=username)
    y=my_profile.id
    myP=Profile.objects.get(id=y)
    return render(request, 'accounts/profile.html',{'my_profile':myP})
