from random import randint
from time import timezone

from django.core.paginator import Paginator
from django.http import JsonResponse, FileResponse, HttpResponse, HttpResponseRedirect, HttpRequest
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, View
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


def random_int():
    random_ref = randint(0, 9999999999)
    uid = random_ref
    return uid


class LearnerRegistration(LoginRequiredMixin, CreateView):

    model = Learner
    form_class = LearnerForm
    template_name = 'forms/learner.html'
    success_url = reverse_lazy('course_reg:s_home')

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST)
        form = form.save(commit=False)
        form.learner_id = random_int()
        course = Course.objects.get(name=form.course)
        form.price = course.price

        form.save()
        # messages.success(self.request, 'Post was successfully added')
        # return redirect('store:s_home')
        learner = Learner.objects.get(learner_id=form.learner_id)
        payment = Payment(learner=learner, amount=learner.course.price, email=learner.email)
        payment.save()
        # payment = Payment.objects.get(learner=learner)

        # return HttpResponseRedirect(reverse('course_reg:initiate_payment', kwargs={'learner_id': learner.learner_id}))
        # return render(self.request, 'forms/initiate_payment.html', {'learner': learner})
        # print(settings.PAYSTACK_PUBLIC_KEY)

        return render(self.request, 'make_payment.html',
                      {'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})

    def form_invalid(self, form, *args, **kwargs):
        # print(self.request.POST)
        print(form.errors)
        # messages.success(self.request, 'Post was not added, ensure that you filled the form correctly')
        return render(self.request, 'forms/learner.html', {'form': form})


def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
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
