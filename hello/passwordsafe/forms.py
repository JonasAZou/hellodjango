from django import forms

class RegistryForm(forms.Form):
    loginname = forms.CharField(max_length=50, min_length=6)
    password = forms.CharField(max_length=100, min_length=6)
    repasswd = forms.CharField(max_length=100, min_length=6)
    email = forms.EmailField()


