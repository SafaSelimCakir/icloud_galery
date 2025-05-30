from django import forms

class ICloudLoginForm(forms.Form):
    email = forms.EmailField(label="Apple ID")
    password = forms.CharField(widget=forms.PasswordInput)


class TwoFactorForm(forms.Form):
    code = forms.CharField(label="2FA Kodu", max_length=6)
