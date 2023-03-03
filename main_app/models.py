from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
from django.urls import reverse


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"


class Author(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    TITLE = (
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
        ('Ms', 'Ms'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="author", blank=True)
    uid = models.SlugField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=7, choices=GENDER, null=True, blank=True)
    title = models.CharField(max_length=7, default='', choices=TITLE, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default="media/profile_pix.png", null=True, blank=True)
    reg_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Activity(models.Model):
    TYPE = (
        ('Login', 'Login'),
        ('Logout', 'Logout'),
        ('Add', 'Add'),
        ('Update', 'Update'),
        ('Delete', 'Delete'),
    )
    actor = models.ForeignKey(Author, on_delete=models.CASCADE,
                              related_name="actor", blank=True)
    type = models.CharField(max_length=7, default='', choices=TYPE, null=True, blank=True)
    action = models.CharField(max_length=100, blank=True, null=True)
    action_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor} {self.action_date} {self.type}"


class Slide(models.Model):
    index = models.IntegerField(null=True, blank=True)
    link = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='slides/', default="media/default_slider.jpg", blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    detail = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        ordering = ("index",)

    def __str__(self):
        return f"slide - {self.index}"