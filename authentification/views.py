from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Language, Article
from .forms import ArticleForm  # Make sure to import the ArticleForm
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
    return render(request, 'home.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session["username"] = username
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
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.source_language = form.cleaned_data['language']
            article.keyword = form.cleaned_data['word']
            article.save()
            messages.success(request, "Article created successfully!")
            return redirect('welcome_user')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ArticleForm()
    
    return render(request, 'welcomeuser.html', {'form': form})

@login_required
def account_view(request):
    return render(request, "account_info.html", {'User': request.user})

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