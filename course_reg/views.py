from random import randint
from time import timezone
import json
from django.core.paginator import Paginator
from django.http import JsonResponse, FileResponse, HttpResponse, HttpResponseRedirect, HttpRequest
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
from django.core.mail import send_mail
from django.conf import settings

from .forms import *
from .models import *
from django.db.models import Count
from django.db.models import Q
# from paypal.standard.forms import PayPalPaymentsForm


def random_int():
    random_ref = randint(0, 9999999999)
    uid = random_ref
    return uid


class LearnerRegistration(CreateView):

    model = Learner
    form_class = LearnerForm
    template_name = 'forms/learner.html'
    success_url = reverse_lazy('course_reg:s_home')

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST)
        form = form.save(commit=False)
        form.learner_id = random_int()
        course = Course.objects.get(name=form.course)
        form.vat = 0.3 * course.price
        form.price = course.price + form.vat

        form.save()
        # messages.success(self.request, 'Post was successfully added')
        # return redirect('store:s_home')
        learner = Learner.objects.get(learner_id=form.learner_id)
        payment = Payment(learner=learner, amount=learner.price, email=learner.email)
        payment.save()
        # payment = Payment.objects.get(learner=learner)

        # return HttpResponseRedirect(reverse('course_reg:initiate_payment', kwargs={'learner_id': learner.learner_id}))
        # return render(self.request, 'forms/initiate_payment.html', {'learner': learner})
        print(settings.PAYPAL_CLIENT_ID)
        print(payment.ref)
        paypal_dict = {
            "business": '',
            "amount": payment.amount,
            "currency_code": "CAD",
            "item_name": f"{payment.learner.course}-{payment.email}",
            "invoice": 2345,
            "notify_url": '',
            "return_url": '',
            "cancel_url": '',
            "lc": 'EN',
            "no_shipping": '1'
        }

        return render(self.request, 'make_payment.html',
                      {'payment': payment, 'paypal_client_is': settings.PAYPAL_CLIENT_ID})
        # form = PayPalPaymentsForm(initial=paypal_dict)
        # return render(self.request, 'forms/paypal_form.html', {'form': form})

    def form_invalid(self, form, *args, **kwargs):
        # print(self.request.POST)
        print(form.errors)
        # messages.success(self.request, 'Post was not added, ensure that you filled the form correctly')
        return render(self.request, 'forms/learner.html', {'form': form})


def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    learner = Learner.objects.get(learner_id=payment.learner.learner_id)
    payment.verified = True
    payment.save()
    learner.paid = True
    learner.save()
    # return redirect('course_reg:payment_completed')
    return render(request, 'payment_completed.html')


class IntroToPython(View):

    def get(self, *args, **kwargs):
        name = 'Intro to Python'
        course = Course.objects.get(name=name)
        # slides = Slide.objects.all()
        # product_cats = ProductCategory.objects.all()
        # product_images = ProductImage.objects.filter(lead=True)

        context = {
            'course': course,
            # 'slides': slides,
            # 'product_cats': product_cats,
            # 'product_images': product_images,
        }

        return render(self.request, 'courses/intro_to_python.html', context)


def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    # student = Student.objects.get(lib_no=body['student'])
    # student.lib_due = True
    # student.save()
    # LibraryDue.objects.create(
    #     student=student
    # )
    payment = get_object_or_404(Payment, ref=body['ref'])
    #Handle this verification its wrong and may be unnecessary
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'Verification successful')
        learner = Learner.objects.get(learner_id=payment.learner.learner_id)
        learner.paid = True
        learner.save()
        return redirect('course_reg:s_home')
    else:
        messages.error(request, 'Verification failed, please try again!')
        return render(request, 'make_payment.html',
                      {'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    # return JsonResponse('Payment completed!', safe=False)

#
# class PayPalFormView(FormView):
#     template_name = 'forms/paypal_form.html'
#     form_class = PayPalPaymentsForm
#
#     def get_initial(self):
#         return {
#             "business": '',
#             "amount": 20,
#             "currency": "CAD",
#             "item_name": '',
#             "invoice": 2345,
#             "notify_url": self.request.build_absolute_url(reverse('')),
#             "return_url": self.request.build_absolute_url(reverse('paypal-return')),
#             "cancel_url": self.request.build_absolute_url(reverse('paypal-cancel')),
#             "lc": 'EN',
#             "no_shipping": '1'
#         }
#

def payment_completed(request):
    return render(request, 'payment_completed.html')


def payment_failed(request):
    return render(request, 'payment_failed.html')