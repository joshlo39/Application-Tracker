from datetime import date
from .models import Internship, UserProfile, Job, JobInterview, ApplicantJob, Applicant, Manager
from rest_framework import serializers


""""
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = UserProfile
        fields = ['user_id','username','password','email']

class ApplicantSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Applicant
        fields = ['points_scored']
"""

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 50)
    email = serializers.EmailField()
    is_applicant = serializers.BooleanField()
    is_manager = serializers.BooleanField()

    class Meta:
        model = UserProfile
        fields = '__all__'

class ApplicantSerializer(serializers.Serializer):
    user = UserSerializer()
    points_scored = serializers.IntegerField()

class ManagerSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Manager
        fields = ['user_id','username','password','email','company']

class JobSerializer(serializers.Serializer):
    job_name = serializers.CharField(max_length=100)
    company = serializers.CharField(max_length=100)
    position = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    date_posted = serializers.DateField(default=date.today)
    job_status = serializers.CharField(max_length=100)

class ApplicantJobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = ApplicantJob
        fields = ['job_id','company','position', 'date_posted','application_status']
        
class JobInterviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = JobInterview
        fields = ['interview_id','job_id','date','type_of_interview','dsa_question']

class InternshipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Internship
        fields = ['internship_name', 'company', 'position', 'date_posted', 'internship_status']
  