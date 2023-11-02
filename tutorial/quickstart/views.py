from django.shortcuts import render
from django.http import HttpResponse
from django.urls import is_valid_path
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ApplicantSerializer, UserSerializer, JobSerializer
from .models import UserProfile, Job
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.generic import CreateView
from django.contrib.auth import login
from django.shortcuts import redirect
from tutorial.quickstart import serializers

def index(request):
    return HttpResponse("Home Page")

def users(request):
    if request.method == 'GET':
        users = UserProfile.objects.all().values()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)


class JobListView(APIView):
    #list all jobs, or create a new job listing.
    def get(self, request, format=None):
        jobs = Job.objects.all()
        serializer_context={'request': request}
        serializer = JobSerializer(jobs, context=serializer_context, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_created)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#class ApplicantJobsView(APIView):

class UserProfileView(APIView):
    def get(self, request, format=None):
        user = UserProfile.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplicantSignupView(APIView):
        
    def post(self, request):
        userserializer = UserSerializer(data=request.data)
        if userserializer.is_valid():
            userserializer.save()
        applicantserializer = ApplicantSerializer(data=request.data)
        if applicantserializer.is_valid():
            applicantserializer.save()
            return Response(applicantserializer.data, status=status.HTTP_201_CREATED)
        return Response(applicantserializer.errors, status=status.HTTP_400_BAD_REQUEST)
