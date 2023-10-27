from tutorial.quickstart.models import User, Job, Interview
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = User
        fields = ['user_id','username','password','email','points_scored']

class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Job
        fields = ['job_id','user_id','company','position','date_applied','status','points']
        
class InterviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Interview
        fields = ['interview_id','job_id','date','type_of_interview','dsa_question']
        