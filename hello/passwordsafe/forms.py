from django import forms

class RegistryForm(forms.Form):
    loginname = forms.CharField(max_length=50)
    password = forms.CharField()


