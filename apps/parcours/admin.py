from django.contrib import admin
from .models import Parcours, Module, Course, Test, UserProgress

admin.site.register(Parcours)
admin.site.register(Module)
admin.site.register(Course)
admin.site.register(Test)
admin.site.register(UserProgress)