from django import forms
from django.forms import ModelForm, Textarea, TextInput, ClearableFileInput, MultipleChoiceField, \
    CheckboxSelectMultiple, Select, CheckboxInput, SelectMultiple
from django.utils.translation import gettext_lazy as _
from .models import *
from django.contrib.auth.forms import UserCreationForm


class LearnerForm(ModelForm):
    class Meta:
        model = Learner
        field = '__all__'
        exclude = ['learner_id', 'price', 'vat', 'created_at', 'paid']

        widgets = {
            'course': Select(attrs={
                'class': 'form__cat__item',
            }),

        }