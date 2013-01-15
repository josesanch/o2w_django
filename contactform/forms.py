from django import forms
from models import Submit

class ContactForm(forms.ModelForm):
    class Meta:
        model = Submit
        exclude = ('form',)
