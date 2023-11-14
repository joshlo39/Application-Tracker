"""
URL configuration for tutorial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from .quickstart import views


urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login_view),
    path('users/', views.UserProfileView.as_view()), 
    path('admin/', admin.site.urls),
    path('jobs/post/', views.JobListView.as_view()),
    path('jobs/', views.JobListView.as_view()), #all jobs
    path('jobs/state/<str:input_state>/',views.JobListView.as_view()), #filter by state
    path('jobs/city/<str:input_city>/',views.JobListView.as_view()), #filter by city
    path('jobs/state/<str:input_state>/city/<str:input_city>',views.JobListView.as_view()),
    path('jobs/open/', views.view_open),    
    path('internships/', views.InternshipListView.as_view()),    
    path('internships/post/', views.InternshipListView.as_view()),    
    path('accounts/', include('django.contrib.auth.urls')),



]