#-*- encoding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from .models import Password

class RegistryForm(forms.Form):
    loginname = forms.CharField(max_length=50, min_length=6)
    password = forms.CharField(max_length=100, min_length=6, widget=forms.PasswordInput)
    repasswd = forms.CharField(max_length=100, min_length=6, widget=forms.PasswordInput)
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super(RegistryForm, self).clean()
        if not cleaned_data['password'] or not cleaned_data['repasswd'] or\
           cleaned_data['password'] != cleaned_data['repasswd']:
            self._errors['repasswd'] = self.error_class([u'两次密码不一致'])
        return cleaned_data

class LoginForm(forms.Form):
    name = forms.CharField(max_length=50, min_length=6)
    password = forms.CharField(max_length=100, min_length=6, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        name = cleaned_data.get('name', None)
        password = cleaned_data.get('password', None)
        if name and password:
            user = authenticate(username=name, password=password)
            if user is None:
                raise forms.ValidationError(u'用户名密码不匹配')
            elif user.is_active:
                cleaned_data['user'] = user
            else:
                raise forms.ValidationError(u'账号已被停用')
        return cleaned_data

class PasswordForm(forms.ModelForm):
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

    class Meta:
        model = Password
        fields = ('loginname', 'password', 'site', 'hint')
        widgets = {
            #'password': forms.PasswordInput,
            'hint': forms.Textarea(attrs={'cols':60, 'rows':10}),
        }


