from datetime import date
from .models import Internship, Resume, UserProfile, Job, JobInterview, ApplicantJob, Applicant, Manager, ApplicantInternship, InternshipInterview
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class ApplicantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Applicant
        fields = '__all__'

class ManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Manager
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = '__all__'

class ApplicantJobSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ApplicantJob
        fields = '__all__'
        
class JobInterviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = JobInterview
        fields = ['interview_id','job_id','date','type_of_interview','dsa_question']

class ApplicantInternshipSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ApplicantInternship
        fields = '__all__'

class InternshipInterviewSerializer(serializers.ModelSerializer):
    class Meta: 
        model = InternshipInterview
        fields = '__all__'

class ResumeSerializer(serializers.ModelSerializer):
    applicant = ApplicantSerializer()
    class Meta: 
        model = Resume
        fields = '__all__'