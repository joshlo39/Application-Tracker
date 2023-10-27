from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

#User class for the user model
class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    points_scored = models.IntegerField(default=0)
    
class Job(models.Model):
    status_choices = [
        ("Applied", "Applied"),
        ("Coding Assessment", "Coding Assessment"),
        ("Interview", "Interview"),
        ("Offer Receieved", "Offer Receieved"),
        ("Rejected", "Rejected"),
        ("Ghosted", "Ghosted")
    ]
    job_id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    date_applied = models.DateField()
    #status = models.CharField(max_length=50,choices = status_choices)
    status = models.CharField(max_length=100)
    points = models.IntegerField
    
class Interview(models.Model):
    type_choices = [
        ("Phone", "Phone"),
        ("Behavioral", "Behavioral"),
        ("Technical", "Technical"),
        ("Onsite", "Onsite"),
        ("System Design", "System Design")
    ]
    interview_id= models.IntegerField(primary_key=True)
    job_id = models.ForeignKey(Job,on_delete=models.CASCADE)
    date = models.DateField()
    #type_of_interview = MultiSelectField(choices = type_choices)
    type_of_interview = models.CharField(max_length=100)
    dsa_question = models.CharField(max_length = 100,blank=True, null = True)
    
    