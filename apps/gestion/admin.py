from django.contrib import admin
from .models import Task, Campaign, Ticket

admin.site.register(Task)
admin.site.register(Campaign)
admin.site.register(Ticket)