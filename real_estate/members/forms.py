from django import forms
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Agent,City,Property,PropertyImage


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    
    SIGNUP_OPTIONS = [
        ('option1', 'Regular Signup'),
        ('option2', 'Agent Signup'),
    ]
    signup_option = forms.ChoiceField(choices=SIGNUP_OPTIONS, widget=forms.RadioSelect, label="Signup Type")

    license_number = forms.CharField(required=False, label='License Number', widget=forms.TextInput(attrs={'placeholder': 'License Number'}))
    phone = forms.CharField(required=False, label='Phone', widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
    # city = forms.CharField(required=False, label='City', widget=forms.TextInput(attrs={'placeholder': 'City'}))
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'signup_option', 'license_number', 'phone', 'city']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        if email and User.objects.filter(email=email).exists():
            self.add_error('email', "Email already exists")

        if username and User.objects.filter(username=username).exists():
            self.add_error('username', "Username already exists")

        if not first_name:
            self.add_error('first_name', "First name is required.")
        if not last_name:
            self.add_error('last_name', "Last name is required.")

        if cleaned_data.get("signup_option") == 'option2':
            if not cleaned_data.get("license_number"):
                self.add_error('license_number', "License Number is required for Agent Signup.")
            if not cleaned_data.get("phone"):
                self.add_error('phone', "Phone is required for Agent Signup.")
            if not cleaned_data.get("city"):
                self.add_error('city', "City is required for Agent Signup.")

        return cleaned_data

class PropertyForm(forms.ModelForm):
    property_id = forms.IntegerField(
        label='Property ID',
        widget=forms.TextInput(attrs={'placeholder': 'Enter Property ID'}),
        required=True
    )
    class Meta:
        model = Property
        fields = ['address', 'city', 'price', 'property_type', 'is_rented']
        widgets = {
            'price': forms.TextInput(attrs={
                'placeholder': 'Enter price',
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Enter price'"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].help_text = "If for rent, write rent per month."


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'description']

PropertyImageFormSet = modelformset_factory(PropertyImage, form=PropertyImageForm, extra=1)


class AgentSearchForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), label="Select City")