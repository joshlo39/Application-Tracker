from .models import UserProfile, Job, JobInterview, ApplicantJob, Applicant, Manager
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = UserProfile
        fields = ['user_id','username','password','email']

class ApplicantSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Applicant
        fields = ['points_scored']

class ManagerSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Manager
        fields = ['company']

class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = ['job_name', 'company', 'position', 'date_posted', 'job_status']

class ApplicantJobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = ApplicantJob
        fields = ['job_id','company','position', 'date_posted','application_status']
        
class JobInterviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = JobInterview
        fields = ['interview_id','job_id','date','type_of_interview','dsa_question']
        