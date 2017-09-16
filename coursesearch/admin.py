from django.contrib import admin
from .models import Course, Subject, Interest, Profile, Grade

# Register your models here.
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Interest)
admin.site.register(Profile)
admin.site.register(Grade)
