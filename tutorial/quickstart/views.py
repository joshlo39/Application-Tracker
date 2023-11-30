
from ast import Delete
#from asyncio.windows_events import NULL
from cgi import print_form
from multiprocessing import managers
from pickle import GET
from pickletools import read_int4
import stat
from sys import intern
from django.core.exceptions import ObjectDoesNotExist
from django.forms import NullBooleanField
from django.http import HttpResponse
from django.urls import is_valid_path
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ApplicantSerializer, InternshipSerializer, InterviewInvitationSerializer, ManagerSerializer, ResumeSerializer, UserSerializer, JobSerializer
from .models import Applicant, ApplicantInternship, ApplicantJob, Internship, InterviewInvitation, Manager, Resume, UserProfile, Job,JobInterview,InternshipInterview
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError 
from django.shortcuts import render
from django.contrib.auth.models import login_required
from datetime import datetime
from .models import Interview
from django.utils import timezone


def index(request):
    return HttpResponse("Gamified Job Application Tracker")

@api_view(['GET'])
def view_mgmt(self):
    users = UserProfile.objects.filter(is_manager=True)
    managers = Manager.objects.filter(user__in=users)
    if users:
        serializer=ManagerSerializer(managers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response("No Managers Found", status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_all_applicants(self):
    users = UserProfile.objects.filter(is_applicant=True)
    all_applicants = Applicant.objects.filter(user__in=users)
    if users:
        serializer=ApplicantSerializer(all_applicants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response("No Applicants Found", status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_open(self):
    jobs = Job.objects.filter(job_status="Open")
    if not jobs:
            return Response("No open jobs currently avaliable")
    else:
        serializer = JobSerializer
        return JsonResponse(serializer)


class UserProfileView(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            user = request.user
            if not request.user.is_staff:  #If not admin, restrict to the logged-in user
                user_profile = UserProfile.objects.get(username=user.username)
            else:
                user_profile = UserProfile.objects.all()
            # Check if user_profile is a single instance or a queryset
            if isinstance(user_profile, UserProfile):
                serializer = UserSerializer(user_profile)
            else:
                serializer = UserSerializer(user_profile, many=True)
            return Response(serializer.data)
        else:
            return Response("Please log in or create an account to view your profile.")


    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = request.data.get('password')
            cur_user = serializer.save()
            cur_user.set_password(password)
            cur_user.save()
            if (cur_user.is_applicant):
                    Applicant.objects.create(user=cur_user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif (cur_user.is_manager):
                    Manager.objects.create(user=cur_user)
                    login(request, cur_user)
                    return redirect('/register/manager_account/')            
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def set_company(request):
    user = request.user
    manager = Manager.objects.get(user=user)
    company = request.data.get('company')
    manager.company = company
    manager.save()
    return Response("Company successfully added")

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print(f"Attempting to authenticate with username: {username}, password: {password}") 
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response("Login Successful")
        # Redirect to a success page.
    else:
        return Response("Invalid Login Credentials")

@api_view(['GET'])
def logout_view(request):
    logout(request)
    return Response("You have been logged out.")

class JobListView(APIView):
    #list all jobs, or create a new job listing.
    def get(self, request, input_state=None, input_city=None):
        try:
            jobs = Job.objects.filter(job_status__contains="Open")
            print(jobs)
            if input_state and input_city:
                jobs = jobs.filter(state=input_state, city=input_city)
            elif input_state:
                jobs = jobs.filter(state=input_state)
            elif input_city:
                jobs = jobs.filter(city=input_city)

            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            # Handle specific validation errors (e.g., invalid filter parameters)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Handle any other kind of exception
            # This is a catch-all for unexpected errors
            return Response({'error': 'Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            if request.user.is_manager:
                manager = Manager.objects.get(user=user)
                manager_id = manager.id
                request.data['hiring_manager'] = manager_id
                serializer = JobSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if request.user.is_staff:
                serializer = JobSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Must be logged into Manager Profile to post a Job Listing")
    
    
class InternshipListView(APIView):    
    def get(self, request, input_state=None, input_city=None):
        try:
            internships = Internship.objects.filter(internship_status__contains="Open")
            print(internships)
            if input_state and input_city:
                internships = internships.filter(state=input_state, city=input_city)
            elif input_state:
                internships = internships.filter(state=input_state)
            elif input_city:
                internships = internships.filter(city=input_city)

            serializer = InternshipSerializer(internships, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            # Handle specific validation errors (e.g., invalid filter parameters)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            if request.user.is_manager:
                manager = Manager.objects.get(user=user)
                manager_id = manager.id
                request.data['hiring_manager'] = manager_id
                serializer = InternshipSerializer(data=request.data)                
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if request.user.is_staff:
                serializer = InternshipSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)             
            else:
                return Response("Must be logged into a Manager Profile to post an Internship Listing")

class InternshipDetailView(APIView):
    def get(self, request, internship_id):
        internships = Internship.objects.filter(internship_id=internship_id)
        if internships:
            internship = Internship.objects.get(internship_id=internship_id)
            serializer = InternshipSerializer(internship)
            if serializer.is_valid:
                return Response(serializer.data)
            else:
                return Response("Error loading Internship", status=status.HTTP_400_BAD_REQUEST)
        return Response("No internship with that ID.", status=status.HTTP_404_NOT_FOUND)

class JobDetailView(APIView):
    def get(self, request, job_id):
        jobs = Job.objects.get(job_id=job_id)
        serializer = JobSerializer(jobs)
        if serializer.is_valid:
            return Response(serializer.data)
        else:
            return Response("Error loading Job", status=status.HTTP_400_BAD_REQUEST)

class my_jobs(APIView):
    def get(self, request):
       if request.user.is_authenticated:
            user = request.user
            if request.user.is_manager:
                manager = Manager.objects.get(user = user)
                jobs = Job.objects.filter(hiring_manager = manager)
                serializer = JobSerializer(jobs, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("Must be logged into a Manager Profile to view your Company Listings.")
            
    def delete(self, request, job_id):
        if request.user.is_authenticated:
            user = request.user
            if request.user.is_manager:
                manager = Manager.objects.get(user = user)
                job = Job.objects.get(job_id = job_id)
                if (job.hiring_manager == manager):
                    return Response("Job deleted", status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response("Must be logged into a Manager Profile to modify your Company Listings.")
        return Response("Authentication Error. Login and try again")
    
    def patch(self, request):
       if request.user.is_authenticated:
            user = request.user
            if request.user.is_manager:
                manager = Manager.objects.get(user=user)
                manager_id = manager.id
                request.data['hiring_manager'] = manager_id
                serializer = JobSerializer(data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("Invalid Credentials", status=status.HTTP_401_UNAUTHORIZED)

class my_internships(APIView):
    def get(self, request):
       if request.user.is_authenticated:
            user = request.user
            if request.user.is_manager:
                manager = Manager.objects.get(user = user)
                internships = Internship.objects.filter(hiring_manager = manager)
                serializer = InternshipSerializer(internships, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("Must be logged into a Manager Profile to view your Company Listings.")
            
    def delete(self, request, internship_id):
        if request.user.is_authenticated:
            user = request.user
            if request.user.is_manager:
                manager = Manager.objects.get(user = user)
                test_internship = Internship.objects.filter(internship_id=internship_id)
                if not test_internship:
                    return Response("Internship ID does not exist.")
                internship = Internship.objects.get(internship_id=internship_id)
                if (internship.hiring_manager == manager):
                    internship.delete()
                    # Internship.objects.delete(internship)
                    return Response("Internship deleted", status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response("Must be logged into a Manager Profile to modify your Company Listings.")
        return Response("Authentication Error. Login and try again")
    
    def patch(self, request):
       if request.user.is_authenticated:
            user = request.user
            if request.user.is_manager:
                manager = Manager.objects.get(user=user)
                manager_id = manager.id
                request.data['hiring_manager'] = manager_id
                serializer = InternshipSerializer(data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("Invalid Credentials", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
def ApplyView(request, job_id):
    if request.user.is_authenticated:
        if request.user.is_applicant:
            applicant = Applicant.objects.get(user=request.user)
            job = Job.objects.get(job_id = job_id)
            job.job_applicants.add(applicant)
            application_check = ApplicantJob.objects.filter(job_id=job, user_id=request.user)
            if not application_check:
                ApplicantJob.objects.create(job_id=job, application_status="Applied", user_id=request.user)
                return Response("Successfully Applied", status=status.HTTP_202_ACCEPTED)
            return Response("Error: You have already applied for this job.", status=status.HTTP_400_BAD_REQUEST)
    return Response("Error with application. Ensure you are signed in to an applicant profile,"
                        " and that the job listing is open", status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def AddResumeView(request):
    if request.user.is_authenticated:
        if request.user.is_applicant:
            cur_applicant = Applicant.objects.get(user=request.user)
            existing_resume = Resume.objects.filter(applicant=cur_applicant)
            print(existing_resume)
            if not existing_resume:
                resume = request.data['resume']
                Resume.objects.create(applicant=cur_applicant, resume=resume)
                return Response("Successfully Added Resume", status=status.HTTP_202_ACCEPTED)
            else:
                return Response("Only one Resume can be added per account.") 
        return Response("Please log into an Applicant Account")
    return Response("Error with authentication. Login again.")  
    
@api_view(['GET'])
def view_applicants(request, job_id):
    if request.user.is_authenticated:
        user = request.user
        if request.user.is_manager:
            manager = Manager.objects.get(user=user)
            job = Job.objects.get(job_id=job_id)
            applicants = job.job_applicants.all()
            if job.hiring_manager == manager:
                serializer = ApplicantSerializer(applicants, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("Error loading Applicants", status=status.HTTP_400_BAD_REQUEST)
    return Response("Please login to view this page", status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def update_job_application_status(request, job_id, applicant_id):
    
    if request.user.is_authenticated:
        user = request.user
        if request.user.is_manager:
            manager = Manager.objects.get(user=user)
            job = Job.objects.get(job_id=job_id)
            print(manager)
            print(job.hiring_manager)
            if job.hiring_manager == manager:
                applicant = Applicant.objects.get(id=applicant_id)
                user = applicant.user
                applicant_job = ApplicantJob.objects.filter(job_id=job, user_id=user)
                if applicant_job:
                    new_status = request.data['Status']
                    try:
                        applicant_job.job_status=new_status
                    except ValidationError:
                        return Response("Invalid Status. Valid Options: "
                                        "Applied, Coding Assessment, Interview,"
                                         " Offer Received, Rejected", status=status.HTTP_400_BAD_REQUEST)
                    return Response("Status Updated", status=status.HTTP_202_ACCEPTED)
                else:
                    return Response("This applicant has not applied to this job", status=status.HTTP_400_BAD_REQUEST)
            return Response("Login to Correct Manager Profile", status=status.HTTP_401_UNAUTHORIZED)
        return Response("Login to Manager Profile", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def view_internship_applicants(request, internship_id):
    if request.user.is_authenticated:
        user = request.user
        if request.user.is_manager:
            manager = Manager.objects.get(user=user)
            internship = Internship.objects.get(internship_id=internship_id)
            applicants = internship.internship_applicants.all()
            print(manager)
            print(internship.hiring_manager)
            if internship.hiring_manager == manager:
                serializer = ApplicantSerializer(applicants, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("Error loading Applicants", status=status.HTTP_400_BAD_REQUEST)
    return Response("Please login to view this page", status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def InternApplyView(request, internship_id):
    if request.user.is_authenticated:
        if request.user.is_applicant:
            applicant = Applicant.objects.get(user=request.user)
            internships = Internship.objects.filter(internship_id = internship_id)
            if internships:
                internship = Internship.objects.get(internship_id = internship_id)
                internship.internship_applicants.add(applicant)
                application_check = ApplicantInternship.objects.filter(internship_id=internship, user_id=request.user)
                if not application_check:
                    ApplicantInternship.objects.create(internship_id=internship, application_status="Applied", user_id=request.user)
                    return Response("Successfully Applied", status=status.HTTP_202_ACCEPTED)
                else:
                    return Response("Error: You have already applied for this internship.", status=status.HTTP_400_BAD_REQUEST)
    return Response("Error with application. Ensure you are signed in to an applicant profile,"
                        " and that the internship listing is open", status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def view_applicant_interviews(request,applicant_id):
    try: 
        applicant = Applicant.objects.get(id=applicant_id)
        
                # Fetch job interviews
        job_interviews = JobInterview.objects.filter(job_id__job_applicants=applicant).values(
            'interview_id', 'job_id__job_name', 'date', 'type_of_interview'
        )
                # Fetch internship interviews
        internship_interviews = InternshipInterview.objects.filter(internship_id__internship_applicants=applicant).values(
            'interview_id', 'internship_id__internship_name', 'date', 'type_of_interview'
        )
        print("applicant exists" + str(applicant))
        totalInterviews = list(job_interviews) + list(internship_interviews)
        return JsonResponse({"interviews": totalInterviews}, status=status.HTTP_200_OK)
    except Applicant.DoesNotExist:
        return JsonResponse({'error': 'The applicant does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET'])
def get_list_of_applied_jobs(request, applicant_id):
    try:
        applicant = Applicant.objects.get(id=applicant_id)
        jobs = Job.objects.filter(job_applicants=applicant)
        serializer = JobSerializer(jobs, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    except Applicant.DoesNotExist:
        return JsonResponse({'error': 'The applicant does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def test_update_applicant_points(request,applicant_id):
    applicant = Applicant.objects.get(id=applicant_id)
    print(applicant.user.email)
    update_applicant_points( applicant_id, 10)
    return JsonResponse({'message': 'Points updated successfully'}, status=status.HTTP_200_OK)
@api_view(['GET'])
def view_amount_of_points(request,applicant_id):
    applicant = Applicant.objects.get(id=applicant_id)
    if applicant:
        return JsonResponse({'points': applicant.points_scored}, status=status.HTTP_200_OK)
    return JsonResponse({'error': 'The applicant does not exist'}, status=status.HTTP_404_NOT_FOUND)
def update_applicant_points(applicant_id,num_of_points):
    applicant = Applicant.objects.get(id=applicant_id)
    if applicant:
        applicant.points_scored = num_of_points
        applicant.save()
        return JsonResponse({'message': 'Points updated successfully'}, status=status.HTTP_200_OK)
    else:
        JsonResponse({'error': 'The applicant does not exist'}, status=status.HTTP_404_NOT_FOUND)

@login_required
def upcoming_interviews(request):
    current_date = datetime.now()
    manager_id = request.user.id
    upcoming_interviews = Interview.objects.filter(applicant__manager_id=manager_id, scheduled_date__gte=current_date)
    return render(request, 'upcoming_interviews.html',{'interviews': upcoming_interviews})

@api_view(['GET'])
def view_interview_invitations(request, user_id):
    try:
        invitations = InterviewInvitation.objects.filter(user_id=user_id)
        serializer = InterviewInvitationSerializer(invitations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except InterviewInvitation.DoesNotExist:
        return Response("No interview invitations found", status=status.HTTP_404_NOT_FOUND)
    
@login_required
def upcoming_interviews(request):
    current_datetime = timezone.now()
    upcoming_interviews = Interview.objects.filter(interview_datetime__gt=current_datetime)
    return render(request, 'interviews/upcoming_interviews.html', {'upcoming_interviews': upcoming_interviews})
    