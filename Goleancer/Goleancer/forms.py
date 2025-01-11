from django import forms
from .models import userchoices

class UserChoicesForm(forms.ModelForm):
    class Meta:
        model = userchoices
        fields = ['name', 'email', 'phone_number', 'image']
