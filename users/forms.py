#encoding:utf-8
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=25, label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=25, help_text = _('Repeat the password'), label=_('Password'), widget=forms.PasswordInput)

    class Meta:
        exclude = ('last_login', 'is_staff', 'is_active',
                   'is_superuser', 'date_joined', 'groups', 'user_permissions')
        model = User

    def clean(self):
        if 'username' in self.cleaned_data:
            if User.objects.filter(username=self.cleaned_data['username']):
                raise forms.ValidationError(_('There is another user with this username, please choose another one.'))


        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_('Passwords are not the same'))

        return self.cleaned_data
