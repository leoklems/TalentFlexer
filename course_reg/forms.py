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
                'class': 'course__reg__form__select',
                'id': 'course',
            }),

        }


class PaymentForForm(ModelForm):
    class Meta:
        model = Learner
        fields = ['learner_id']


class PaymentForm(forms.Form):
    card_number = forms.CharField(label='Card number', max_length=16)
    exp_month = forms.CharField(label='Expiration month', max_length=2)
    exp_year = forms.CharField(label='Expiration year', max_length=4)
    cvc = forms.CharField(label='CVC', max_length=4)
    cardholder_name = forms.CharField(label='Cardholder name', max_length=100)
