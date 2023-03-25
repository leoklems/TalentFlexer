from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'course_reg'

urlpatterns = [
    path('course-registration/', LearnerRegistration.as_view(), name='course_registration'),
    path('payment-completed/', payment_completed, name='payment_completed'),
    path('payment-failed/', payment_failed, name='payment_failed'),
    path('verify/<str:ref>/', verify_payment, name='verify_payment'),
    path('<course_id>/', CourseView.as_view(), name='course'),
]
