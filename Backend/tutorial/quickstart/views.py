from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, JobSerializer, InterviewSerializer
from .models import User, Job, Interview
from django.http import JsonResponse

def users(request):
    if request.method == 'GET':
        users = User.objects.all().values()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
        


