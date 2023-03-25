from random import randint
from time import timezone

from django.core.paginator import Paginator
from django.http import JsonResponse, FileResponse, HttpResponse, HttpResponseRedirect
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

from .forms import *
from .models import *
from course_reg.models import Course
from django.db.models import Count
from django.db.models import Q

# Create your views here.


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,
                            password=password)
        print(user)

        if user is not None:
            login(request, user)
            staff = Author.objects.get(user=request.user)
            act = Activity(actor=staff, action='Login')
            act.save()
            return redirect('store:s_home')

        else:
            messages.info(request, 'username or password is incorrect')

    return render(request, 'forms/login.html')


def logoutUser(request):
    staff = Author.objects.get(user=request.user)
    act = Activity(actor=staff, action='Logout')
    act.save()
    logout(request)
    return redirect('store:login')


class Home(View):

    def get(self, *args, **kwargs):
        slides = Slide.objects.all()
        site_info = SiteSetupModel.objects.get(index=0)
        courses = Course.objects.all()

        context = {
            'slides': slides,
            'site_info': site_info,
            'courses': courses,
        }

        return render(self.request, 'home.html', context)


class CorporateTraining(View):

    def get(self, *args, **kwargs):
        site_info = SiteSetupModel.objects.get(index=0)
        courses = Course.objects.all()

        context = {
            'site_info': site_info,
            'courses': courses,
        }

        return render(self.request, 'corporate_training.html', context)


class GalleryView(View):

    def get(self, *args, **kwargs):
        site_info = SiteSetupModel.objects.get(index=0)
        images = Gallery.objects.all()

        context = {
            'site_info': site_info,
            'images': images,
        }

        return render(self.request, 'gallery.html', context)
