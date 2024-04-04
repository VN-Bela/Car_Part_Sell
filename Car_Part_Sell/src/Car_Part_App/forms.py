from django import forms
from .models import CarPart,CarModel
from django.forms.utils import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.db import  transaction

class Car_Part_Form(forms.ModelForm):
    class Meta:
        model=CarPart
        fields=[
            'name',
            'category',
           
        ]
