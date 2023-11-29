from datetime import date
from django.db import models
from django.forms import CharField, IntegerField
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractUser


#User class for the user model
class UserProfile(AbstractUser):
    is_applicant = models.BooleanField('Applicant Status', default=False)
    is_manager = models.BooleanField('Manager Status', default=False)

    def __str__(self):
        return self.username
    
class Applicant(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    points_scored = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

class Manager(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username

class Job(models.Model):
    job_id = models.AutoField (primary_key=True)
    job_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    date_posted = models.DateField(default=date.today)
    #status = models.CharField(max_length=50,choices = status_choices)
    listing_status = [
        ("Open", "Open"),
        ("Closed", "Closed")
    ]
    job_status = MultiSelectField(choices=listing_status, max_choices=1, max_length=100)
    hiring_manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    job_applicants = models.ManyToManyField(Applicant, null=True, blank=True)
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
    date_applied = models.DateField(default=date.today)
    #status = models.CharField(max_length=50,choices = status_choices)
    application_status = models.CharField(max_length=100, choices=status_choices)
    points = models.IntegerField

    def __str__(self):
        return self.job_id.job_name

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
    internship_name = models.CharField(max_length=100)
    hiring_manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    date_posted = models.DateField(default=date.today)
    #status = models.CharField(max_length=50,choices = status_choices)
    internship_status = models.CharField(max_length=100)
    internship_applicants = models.ManyToManyField(Applicant, null=True, blank=True)

    def __str__(self):
        return self.internship_name 

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
    date_applied = models.DateField(default=date.today)
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

class Resume(models.Model):
    resume_id = models.AutoField(primary_key=True)
    applicant = models.OneToOneField(Applicant, on_delete=models.CASCADE)
    resume = models.TextField(editable=True)
    def __str__(self):
        return self.applicant.user.username 
    


