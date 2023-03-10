from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *

app_name = 'course_reg'

urlpatterns = [
    path('intro-to-python/', IntroToPython.as_view(), name='intro_to_python'),
    path('course-registration/', LearnerRegistration.as_view(), name='course_registration'),
    path('<str:ref>/', views.verify_payment, name='verify_payment')
]
