from django.contrib import admin
from .models import Certificate, JobPosting, JobApplication

admin.site.register(Certificate)
admin.site.register(JobPosting)
admin.site.register(JobApplication)