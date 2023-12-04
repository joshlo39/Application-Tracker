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
from .quickstart.views import upcoming_interviews, view_interview_invitations





urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('register/', views.UserProfileView.as_view()), 
    path('register/manager_account/', views.set_company, name='set_company'), 
    path('users/', views.UserProfileView.as_view()), 
    path('users/managers/', views.view_mgmt), 
    path('users/applicants/', views.view_all_applicants),
    path('profile/', views.UserProfileView.as_view()), 
    path('profile/add_resume/', views.AddResumeView), 
    path('admin/', admin.site.urls),
    path('jobs/', views.JobListView.as_view()), #all jobs
    path('jobs/my_job_offers/', views.JobOfferListView.as_view()), 
    path('jobs/<job_id>/', views.JobDetailView.as_view()),
    path('jobs/<job_id>/applicants/', views.view_applicants),  
    path('jobs/<job_id>/applicants/<applicant_id>/', views.update_job_application_status),      
    path('jobs/<job_id>/apply/', views.ApplyView),
    path('my_jobs/', views.my_jobs.as_view()),
    # path('my_jobs/<job_id>/', views.my_jobs.as_view()),
    path('jobs/state/<str:input_state>/',views.JobListView.as_view()), #filter by state
    path('jobs/city/<str:input_city>/',views.JobListView.as_view()), #filter by city
    path('jobs/state/<str:input_state>/city/<str:input_city>',views.JobListView.as_view()),
    path('jobs/open/', views.view_open),
    path('internships/', views.InternshipListView.as_view()),   
    path('internships/my_internship_offers/', views.InternshipOfferListView.as_view()), 
    path('internships/<internship_id>/', views.InternshipDetailView.as_view()), 
    path('internships/<internship_id>/apply/', views.InternApplyView),     
    path('internships/<internship_id>/applicants/', views.view_internship_applicants),
    path('internships/<internship_id>/applicants/<applicant_id>', views.view_internship_applicants),
    path('my_internships/', views.my_internships.as_view()),
    path('my_internships/<internship_id>/', views.my_internships.as_view()),    
    path('accounts/', include('django.contrib.auth.urls')),
    path('upcoming_interviews/', upcoming_interviews, name='upcoming_interviews'),
    path('jobs/<int:job_id>/apply/', views.ApplyView),
    path('interviews/view_interview_invitations/', views.view_interview_invitations, name='view_interview_invitations'),
    path('api/update_interview_status/<int:interview_id>/', views.update_interview_status, name='update_interview_status'),
    path('api/upcoming_interviews/', upcoming_interviews, name='upcoming_interviews'),



]