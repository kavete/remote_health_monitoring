from django import forms

class LoginForm(forms.ModelForm):
    username = forms.CharField()