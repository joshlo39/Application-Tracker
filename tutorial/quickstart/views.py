
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
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from rest_framework.decorators import api_view

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
        user = UserProfile.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            cur_user = serializer.save()
            if (UserProfile.is_manager):
                    Manager.objects.create(user=cur_user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            if (UserProfile.is_applicant):
                    Applicant.objects.create(user=cur_user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def users(request):
    if request.method == 'GET':
        users = UserProfile.objects.all().values()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def create_profile(request):
    serializer=UserSerializer(data=request.data)
    if (serializer.is_vaid):
        if (serializer.is_manager):
            redirect
            Manager.objects.create(user=serializer)

    
@api_view(['GET', 'POST'])
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    UserProfile = authenticate(request, username=username, password=password)
    if UserProfile is not None:
        login(request, UserProfile)
        # Redirect to a success page.
    else:
        return Response("Invalid Login Credentials")
        
class JobListView(APIView):
    #list all jobs, or create a new job listing.
    def get(self, request):
        jobs = Job.objects.all()
        serializer_context={'request': request}
        serializer = JobSerializer(jobs, context=serializer_context, many=True)
        return Response(serializer.data)
    
    
    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if request.user.is_authenticated:
            if request.user.is_manager:
                Job.hiring_manager = request.user
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_created)
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
        serializer = InternshipSerializer(data=request.data)
        if request.user.is_authenticated:
            if request.user.is_manager:
                Internship.hiring_manager = request.user
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_created)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Must be logged into Manager Profile to post an Internship Listing")
    
   
