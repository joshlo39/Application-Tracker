from django.contrib import admin
from .models import ApplicantInternship, ApplicantJob, Job, JobInterview, Internship, InternshipInterview, Resume, UserProfile, Applicant, Manager
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Job)
admin.site.register(JobInterview)
admin.site.register(Internship)
admin.site.register(InternshipInterview)
admin.site.register(Applicant)
admin.site.register(Manager)
admin.site.register(ApplicantJob)
admin.site.register(ApplicantInternship)
admin.site.register(Resume)
