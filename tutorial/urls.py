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
    path('logout/', views.logout_view),
    path('register/', views.UserProfileView.as_view()), 
    path('register/manager_account/', views.set_company, name='set_company'), 
    path('users/', views.UserProfileView.as_view()), 
    path('profile/', views.UserProfileView.as_view()), 
    path('profile/add_resume/', views.AddResumeView), 
    path('admin/', admin.site.urls),
    path('jobs/', views.JobListView.as_view()), #all jobs
    path('jobs/<job_id>/', views.JobDetailView.as_view()),
    path('jobs/<job_id>/applicants/', views.view_applicants),    
    path('jobs/<job_id>/apply/', views.ApplyView),
    path('my_jobs/', views.my_jobs.as_view()),
    path('my_jobs/<job_id>/', views.my_jobs.as_view()),
    path('jobs/state/<str:input_state>/',views.JobListView.as_view()), #filter by state
    path('jobs/city/<str:input_city>/',views.JobListView.as_view()), #filter by city
    path('jobs/state/<str:input_state>/city/<str:input_city>',views.JobListView.as_view()),
    path('jobs/open/', views.view_open),    
    path('internships/', views.InternshipListView.as_view()),   
    path('internships/<internship_id>/', views.InternshipDetailView.as_view()),   
    path('internships/<internship_id>/applicants/', views.view_internship_applicants),
    path('my_internships/', views.my_internships.as_view()),
    path('my_internships/<internship_id>/', views.my_internships.as_view()),    
    path('accounts/', include('django.contrib.auth.urls')),
]