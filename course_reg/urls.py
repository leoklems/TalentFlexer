from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'course_reg'

urlpatterns = [
    path('course-registration/', LearnerRegistration.as_view(), name='course_registration'),
    path('payment-completed/', payment_completed, name='payment_completed'),
    path('make-payment/', PaymentFor.as_view(), name='make_payment'),
    path('make-payment/<str:learner_id>/', payment_failed, name='payment_failed'),
    path('verify/<str:ref>/', verify_payment, name='verify_payment'),
    path('<course_id>/', CourseView.as_view(), name='course'),
    path('make-payment/validate-learner-id', validate_learner_id, name='validate_learner_id'),
    path('course-registration/validate-email', validate_email, name='validate_email'),
]
