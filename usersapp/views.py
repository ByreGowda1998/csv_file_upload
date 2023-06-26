from django.shortcuts import render,redirect

from django.contrib.auth import get_user_model
User=get_user_model()
from django.contrib import messages
from django.contrib.auth import login ,logout,authenticate 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def homepage(request):
    return render(request,'base.html')

def loginto(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, "You are now login is succesfull")
				return redirect('home')
		else:
				messages.error(request,"Invalid username or password.")    
	form = AuthenticationForm()
	return render(request=request, template_name='login.html', context={"login_form":form}) 


@login_required(login_url='loginto')     
def log_out(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("loginto")