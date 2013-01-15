from django import forms
from django.contrib.auth.models import User
import models

class AddressForm(forms.ModelForm):
    class Meta:
        model = models.Address
        exclude = ('user_shipping', 'user_billing')



class UserForm(forms.ModelForm):
    password2 = forms.CharField(max_length=25)

    class Meta:
        exclude = ('last_login', 'first_name', 'last_name', 'is_staff', 'is_active',
                   'is_superuser', 'date_joined', 'groups', 'user_permissions')
        model = User

