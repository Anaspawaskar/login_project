from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import IntegrityError



# Create your views here.

def home(request):
    return render(request, 'authentication/index.html')

def signup(request):
    try:
        if request.method == "POST":
            username = request.POST['username']
            fname = request.POST['fname']
            lname = request.POST['lname']
            Email = request.POST['Email']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            
            if User.objects.filter(username=username):
                messages.error(request, "please try some other username")
                return redirect('home')

            if User.objects.filter(Email=Email):
                messages.error(request, "Email already Registered")
                return redirect('home')
            
            if len(username)>10:
                messages.error(request,"username must unser 10 characters")

            if pass1 != pass2:
                messages.error(request, "password didn't matches")

            if not username.isalnum():
                messages.error(request, "username must be alpha numeric")
                return redirect('home')
            

            myuser = User.objects.create_user(username, Email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname

            myuser.save()

            messages.success(request, "your account has been successfully created")

            return HttpResponseRedirect('signin')
        
        return render(request, "authentication/signup.html")
    
    except IntegrityError:
        return HttpResponseRedirect('signup')



def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username = username, password = pass1)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname' : fname})

        else:
            messages.error("bad credentials ")
            return redirect('home')




    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"you have successfully logged out.")
    return redirect('home')