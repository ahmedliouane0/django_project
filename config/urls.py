"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Import necessary modules
from django.contrib import admin
from django.urls import path
from authentification.views import *  
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    
    path('', home, name="recipes"),        
    path('home/', home, name='home'),      
    path("admin/", admin.site.urls),       
    path('login/', login_view, name='login_page'),  
    path('register/', register_page, name='register'), 
    path('logout/', logout_view, name='logout'),
    path("welcome/", welcome_user, name="welcome_user"),
    path('account/', account_view, name='account'), 
    path('delete-account/confirm/', delete_account, name='delete_account_confirm'),
    path('delete-account/', delete_account_confirmation, name='delete_account'),
   
    
    
    ]

# Serve media files if DEBUG is True (development mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files using staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
