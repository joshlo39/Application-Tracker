from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

#User class for the user model
class UserProfile(AbstractUser):
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField(max_length=100)
    is_applicant = models.BooleanField('Applicant Status', default=False)
    is_manager = models.BooleanField('Manager Status', default=False)

    def __str__(self):
        return self.username
    
class Applicant(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
    points_scored = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Manager(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
    company = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username

class Job(models.Model):
    job_id = models.AutoField (primary_key=True)
    job_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    date_posted = models.DateField(default=timezone.now)
    #status = models.CharField(max_length=50,choices = status_choices)
    job_status = models.CharField(max_length=100)
    hiring_manager = models.ForeignKey(Manager, on_delete=models.CASCADE)

    def __str__(self):
        return self.job_name 

#split Job model into basic Job listing, with extended ApplicantJob model that has details specific to the applicant. 
class ApplicantJob(models.Model):
    job_id = models.OneToOneField(Job, on_delete=models.CASCADE, primary_key=True)
    status_choices = [
        ("Applied", "Applied"),
        ("Coding Assessment", "Coding Assessment"),
        ("Interview", "Interview"),
        ("Offer Receieved", "Offer Receieved"),
        ("Rejected", "Rejected"),
        ("Ghosted", "Ghosted")
    ]
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date_applied = models.DateField()
    #status = models.CharField(max_length=50,choices = status_choices)
    application_status = models.CharField(max_length=100, choices=status_choices)
    points = models.IntegerField

class JobInterview(models.Model):
    type_choices = [
        ("Phone", "Phone"),
        ("Behavioral", "Behavioral"),
        ("Technical", "Technical"),
        ("Onsite", "Onsite"),
        ("System Design", "System Design")
    ]
    interview_id= models.AutoField (primary_key=True)
    job_id = models.ForeignKey(Job,on_delete=models.CASCADE)
    date = models.DateField()
    #type_of_interview = MultiSelectField(choices = type_choices)
    type_of_interview = models.CharField(max_length=100)
    dsa_question = models.CharField(max_length = 100,blank=True, null = True)
    

class Internship(models.Model):
    internship_id = models.AutoField (primary_key=True)
    hiring_manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    date_posted = models.DateField()
    #status = models.CharField(max_length=50,choices = status_choices)
    internship_status = models.CharField(max_length=100)

class ApplicantInternship(models.Model):
    internship_id = models.OneToOneField(Internship, on_delete=models.CASCADE, primary_key=True)
    status_choices = [
        ("Applied", "Applied"),
        ("Coding Assessment", "Coding Assessment"),
        ("Interview", "Interview"),
        ("Offer Receieved", "Offer Receieved"),
        ("Rejected", "Rejected"),
        ("Ghosted", "Ghosted")
    ]
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date_applied = models.DateField()
    #status = models.CharField(max_length=50,choices = status_choices)
    application_status = models.CharField(max_length=100, choices=status_choices)
    points = models.IntegerField  

class InternshipInterview(models.Model):
    type_choices = [
        ("Phone", "Phone"),
        ("Behavioral", "Behavioral"),
        ("Technical", "Technical"),
        ("Onsite", "Onsite"),
        ("System Design", "System Design")
    ]
    interview_id= models.AutoField (primary_key=True)
    internship_id = models.ForeignKey(Internship, on_delete=models.CASCADE)
    date = models.DateField()
    #type_of_interview = MultiSelectField(choices = type_choices)
    type_of_interview = models.CharField(max_length=100)
    dsa_question = models.CharField(max_length = 100,blank=True, null = True)