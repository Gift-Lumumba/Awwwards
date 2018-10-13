from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude =['posted_on','profile','user']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        fields = ('profile_pic','bio' )