# Import necessary modules and models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Language
import requests
from django.conf import settings
from django.http import JsonResponse
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

 
def home(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    
    context = {
        'user_id': user_id,
        'username': username
    }

    return render(request, 'home.html',context)


from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log in the user
            request.session["username"] = username  # Store username in session
            return redirect("welcome_user")  
        
        else:
            return render(request, "login.html", {"error": "Invalid username or password."})

    return render(request, "login.html")



def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')  
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        
        if not all([first_name, last_name, username, email, password, confirm_password]):
            messages.error(request, "All fields are required!")
            return redirect('/register/')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('/register/')

        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('/register/')

        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use!")
            return redirect('/register/')

        
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,  
            password=password
        )

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('/login/')  

    return render(request, 'register.html')


def logout_view(request):
    logout(request)  
    request.session.flush() 
    messages.success(request, "Logged out successfully!")
    return redirect('/login/')

@login_required(login_url="login_page") 
def welcome_user(request):
    # Fetch all languages 
    languages = Language.objects.all()
    
    context = {
        'languages': languages,
        
    }
    
    return render(request, 'welcomeuser.html', context)


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Article, Language

@login_required(login_url="login_page")
def process_data(request):
    if request.method == 'POST':
        keyword = request.POST.get('word', '').strip()
        subject = request.POST.get('subject', '').strip()
        language_id = request.POST.get('language', '').strip()

        if not keyword or not subject or not language_id:
            messages.error(request, "All fields are required and cannot contain only spaces!")
            return redirect('welcome_user')

        try:
            language = Language.objects.get(id=language_id)
        except Language.DoesNotExist:
            messages.error(request, "Selected language is invalid.")
            return redirect('welcome_user')

        Article.objects.create(
            keyword=keyword,
            subject=subject,
            source_language=language,
            user=request.user
        )

        messages.success(request, "Article created successfully!")
        return redirect('welcome_user')

    return redirect('welcome_user')



def form_view(request):
    languages = Language.objects.all()
    return render(request, "welcomeuser.html", {"languages": languages})


@login_required
def  account_view(request):
    return render(request,"account_info.html",{'User' : request.user})

@login_required
def delete_account_confirmation(request):
    return render(request, 'delete_confirmation.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request) 
        user.delete()
        return redirect('/')      
    return redirect('delete_account')  


