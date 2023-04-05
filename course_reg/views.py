from random import randint
from time import timezone
import json
from django.core.paginator import Paginator
from django.http import JsonResponse, FileResponse, HttpResponse, HttpResponseRedirect, HttpRequest, request
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, View, FormView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from itertools import chain
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings

from .forms import *
from .models import *
from main_app.models import SiteSetupModel
from django.db.models import Count
from django.db.models import Q


# from paypal.standard.forms import PayPalPaymentsForm


def random_int():
    random_ref = randint(0, 9999)
    uid = random_ref
    return uid


class LearnerRegistration(CreateView):
    model = Learner
    form_class = LearnerForm
    template_name = 'forms/learner.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_info = SiteSetupModel.objects.get(index=0)
        courses = Course.objects.all()
        context["site_info"] = site_info
        context["courses"] = courses
        return context

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST.get('course'))
        try:
            learner = Learner.objects.get(email=self.request.POST.get('email'), course__id=self.request.POST.get('course'))
            learner_exists = True
        except:
            learner_exists = False

        if learner_exists:
            site_info = SiteSetupModel.objects.get(index=0)
            courses = Course.objects.all()
            return render(self.request, 'forms/learner.html', {'form': form, 'site_info': site_info, 'courses': courses})
        form = form.save(commit=False)

        # Split the email by the "@" symbol and select the first part
        text_part = form.email.split('@')[0]
        # concatenate the text_part and the randomly generated number
        form.learner_id = f"{text_part}{random_int()}".lower()
        # Select the course from the Course model
        course = Course.objects.get(name=form.course)
        # Calculate and record the VAT
        form.vat = 0.13 * course.price
        # Calculate and record the total cost plus the vat for the course
        form.price = course.price + form.vat

        form.save()
        messages.success(self.request, 'You have been successfully registered')
        learner = Learner.objects.get(learner_id=form.learner_id)
        print(learner.__dict__)
        payment = Payment(learner=learner, amount=learner.price, email=learner.email)
        payment.save()
        domain = get_current_site(request).domain
        # uidb68 = urlsafe_base64_encode(force_bytes(user.pk))
        link = reverse('course_reg:make_payment')
        activate_url = 'http://' + domain + link
        email = self.request.POST.get('email')
        email_subject = "Activate your account"
        fro = settings.EMAIL_HOST_USER
        email_body = "Hi " + str(
            learner) + ", your ID is " + learner.learner_id + ". please use this link to make payment and complete " \
                                                              "your enrollment " + activate_url
        # print(email_body)
        email = EmailMessage(
            email_subject,
            email_body,
            # email_body,
            fro,
            [email],
        )
        email.send(fail_silently=False)

        site_info = SiteSetupModel.objects.get(index=0)
        courses = Course.objects.all()

        return render(self.request, 'make_payment.html',
                      {'site_info': site_info, 'courses': courses, 'payment': payment,
                       'paypal_client_is': settings.PAYPAL_CLIENT_ID})

    def form_invalid(self, form, *args, **kwargs):
        site_info = SiteSetupModel.objects.get(index=0)
        print(form.errors)
        # messages.success(self.request, 'Post was not added, ensure that you filled the form correctly')
        return render(self.request, 'forms/learner.html', {'form': form, 'site_info': site_info})


def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    """
    parameters
    --------------
    request:
    ref: a reference key generated when the payment was initiated which is used here to track the payment
    return: render the payment completed page
    """
    # Get the payment object using the reference
    payment = get_object_or_404(Payment, ref=ref)
    # Get the learner object using the payment
    learner = Learner.objects.get(learner_id=payment.learner.learner_id)
    # Verify that payment has been completed
    payment.verified = True
    # Record the updated payment
    payment.save()
    # Update the payment status of the learner to "paid"
    learner.paid = True
    # Record the updated payment status
    learner.save()
    # return redirect('course_reg:payment_completed')
    return render(request, 'payment_completed.html')


class CourseView(DetailView):
    model = Course
    template_name = 'courses/course.html'
    slug_field = 'course_id'
    slug_url_kwarg = 'course_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_info = SiteSetupModel.objects.get(index=0)
        courses = Course.objects.all()
        context["site_info"] = site_info
        context["courses"] = courses
        return context


class PaymentFor(View):

    def get(self, request):
        site_info = SiteSetupModel.objects.get(index=0)
        courses = Course.objects.all()

        return render(request, 'forms/payment_for.html',
                      {'site_info': site_info, 'courses': courses})

    def post(self, request, *args, **kwargs):
        learner_id = request.POST.get('learner_id')
        learner = Learner.objects.get(learner_id=learner_id)
        payment = Payment.objects.get(learner=learner)
        payment_for_form = PaymentForForm(request.POST)
        site_info = SiteSetupModel.objects.get(index=0)
        courses = Course.objects.all()
        if payment_for_form.is_valid():
            # return redirect('app:register_student')
            return render(self.request, 'make_payment.html',
                          {'site_info': site_info, 'courses': courses, 'payment': payment,
                           'paypal_client_is': settings.PAYPAL_CLIENT_ID})

        else:
            # when the form has an error
            print(payment_for_form.errors)
            messages.success(request, 'Fill out all the necessary details ')
            learner_id = request.GET.get('learner_id', None)
            learner = Learner.objects.get(learner_id=learner_id)
            payment = Payment(learner=learner, amount=learner.price, email=learner.email)
            site_info = SiteSetupModel.objects.get(index=0)
            courses = Course.objects.all()

            return render(request, 'forms/payment_for.html',
                          {'site_info': site_info, 'courses': courses})


def payment_completed(request):
    site_info = SiteSetupModel.objects.get(index=0)
    courses = Course.objects.all()
    return render(request, 'payment_completed.html', {'site_info': site_info, 'courses': courses})


def payment_failed(request: HttpRequest, learner_id: str) -> HttpResponse:
    learner = Learner.objects.get(learner_id=learner_id)
    payment = Payment(learner=learner, amount=learner.price, email=learner.email)
    site_info = SiteSetupModel.objects.get(index=0)
    courses = Course.objects.all()

    return render(request, 'make_payment.html',
                  {'payment': payment, 'site_info': site_info, 'courses': courses,
                   'paypal_client_is': settings.PAYPAL_CLIENT_ID})


def validate_email(request):
    # to check if a user has already registered a chosen email
    # collected by json to ajxa in form.js
    email = request.GET.get('email', None)
    course = request.GET.get('course', None)
    learner = Learner.objects.filter(email__iexact=email).exists()
    data = dict()
    # {
    #     'is_taken': Learner.objects.filter(email__iexact=email).exists()
    # }
    if learner:
        learner = Learner.objects.get(email=email)
        try:
            Learner.objects.get(email=email, course_id=course)
            print(learner)
            data['is_taken'] = 'is_taken'
        except:
            data['is_not_taken'] = 'is_not_taken'
        # if learner.id == course:
        #     data['is_taken'] = 'is_taken'
        # else:
        #     data['is_not_taken'] = 'is_not_taken'
    else:
        data['is_not_taken'] = 'is_not_taken'
    return JsonResponse(data)


def validate_learner_id(request):
    feedback = dict()
    learner_id = request.GET.get('learner_id', None)
    learner = Learner.objects.filter(learner_id__iexact=learner_id).exists()
    if learner:
        learner = Learner.objects.get(learner_id=learner_id)
        if learner.paid:
            feedback['paid'] = 'paid'
        else:
            feedback['not_paid'] = 'not_paid'
    else:
        feedback['non_learner'] = 'non_learner'
    return JsonResponse(feedback)
