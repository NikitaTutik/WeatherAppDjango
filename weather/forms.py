from django import forms
from django.forms import ModelForm
from .models import *


class WeatherForm(ModelForm):

    class Meta:
        model = WeatherModel
        fields = ['city']
