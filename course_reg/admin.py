from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CoursePreRequisite)
admin.site.register(CourseBenefit)
admin.site.register(Course)
admin.site.register(Learner)
admin.site.register(Payment)