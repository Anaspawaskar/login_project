from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.core.mail import send_mail

from app1 import settings



# Create your views here.

def home(request):
    return render(request, 'authentication/index.html')

def signup(request):            #ask for the user information and have some authentication some exception
        
    
        if request.method == "POST":
            username = request.POST['username']
            fname = request.POST['fname']
            lname = request.POST['lname']
            Email = request.POST['Email']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']

        
            
            if User.objects.filter(username = username):
                messages.error(request, "please try some other username")
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

            messages.success(request, "your account has been successfully created, We have sent you an confirmation Email, please confirm your email account")

            # Welcome Email 

            # Subject = "Welcome To my Django login"
            # messages = "Hello " + myuser.first_name + "!! \n" + "Welcome to my Anas!! \n thank you for visiting our website /n we have sent you a confirmation email, please confirm your email address in order to activate your account. /n/n Thanking you /n Anas pawaskar"
            # from_email = settings.EMAIL_HOST_USER
            # to_list = [myuser.email]
            # send_mail(Subject, messages, from_email, to_list, fail_silently = True)

            return redirect('home')
        
    
        
        return render(request, "authentication/signup.html")
    
    
    
    
    
    



def signin(request):            #It sings in the user who have already registered in the system

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

def signout(request):           #This will sih=gn out user from the system but have the records of the user
    logout(request)
    messages.success(request,"you have successfully logged out.")
    return redirect('home')