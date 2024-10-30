from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Agent

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')


    class Meta:
        model = User
        fields = ['username', 'email', 'password' , 'first_name' , 'last_name']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        email = cleaned_data.get("email")
        
        if User.objects.filter(email=email).exists():
            self.add_error('email', "Email already exists")
        
        return cleaned_data

class AgentSignUpForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['license_number', 'phone', 'city']
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Phone'}),
            'license_number': forms.TextInput(attrs={'placeholder': 'License Number'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].required = True
        self.fields['phone'].required = True
        self.fields['license_number'].required = True
