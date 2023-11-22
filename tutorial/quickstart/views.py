
from ast import Delete
from cgi import print_form
from multiprocessing import managers
from pickle import GET
from pickletools import read_int4
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ApplicantSerializer, InternshipSerializer, UserSerializer, JobSerializer
from .models import Applicant, Internship, Manager, UserProfile, Job
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError 

def index(request):
    return HttpResponse("Gamified Job Application Tracker")
    
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
            else:
                return Response("Must be logged into Manager Profile to post a Job Listing")
    
    
class InternshipListView(APIView):
    #list all jobs, or create a new job listing.
    def get(self, request, format=None):
        internships = Internship.objects.all()
        serializer_context={'request': request}
        serializer = InternshipSerializer(internships, context=serializer_context, many=True)
        return Response(serializer.data)
    
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
            else:
                return Response("Must be logged into a Manager Profile to post an Internship Listing")

class JobDetailView(APIView):
    def get(self, request, job_id):
        jobs = Job.objects.get(job_id=job_id)
        serializer = JobSerializer(jobs)
        if serializer.is_valid:
            return Response(serializer.data)
        else:
            return Response("Error loading Job", status=status.HTTP_400_BAD_REQUEST)

class my_jobs(APIView):
    def get(request):
       if request.user.is_authenticated:
            user = request.user
            if request.user.is_manager:
                manager = Manager.objects.get(user = user)
                jobs = Job.objects.filter(hiring_manager = manager)
                serializer = JobSerializer(jobs, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("Must be logged into a Manager Profile to view your Company Listings.")
    
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


@api_view(['PUT'])
def ApplyView(request, job_id):
    if request.user.is_authenticated:
        if request.user.is_applicant:
            applicant = Applicant.objects.get(user=request.user)
            job = Job.objects.get(job_id = job_id)
            print(job_id)
            job.job_applicants.add(applicant)
            return Response("Successfully Applied", status=status.HTTP_202_ACCEPTED)
        return Response("Error with application. Ensure you are signed in to an applicant profile, and that the job listing is open", status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def view_applicants(request, job_id):
    if request.user.is_authenticated:
        user = request.user
        if request.user.is_manager:
            manager = Manager.objects.get(user=user)
            print("Manager:", manager)
            print("1")
            job = Job.objects.get(job_id=job_id)
            print("2")
            applicants = job.job_applicants.all()
            print(type(applicants))

            print("3")
            if job.hiring_manager == manager:
                print("4")
                serializer = ApplicantSerializer(applicants, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("Error loading Applicants", status=status.HTTP_400_BAD_REQUEST)
    return Response("Please login to view this page", status=status.HTTP_401_UNAUTHORIZED)