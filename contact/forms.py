from django import forms
from django.core.exceptions import ValidationError
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ex. Name'
            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ex. LastName'
            }
        )
    )

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ex. +99 (99) 99999-9999'
            }
        )
    )

    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'name@mail.com'
            }
        ),
        label='E-mail'
    )

    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            }
        ),
        required=False
    )

    class Meta:
        model = models.Contact
        fields = (
            'first_name',
            'last_name',
            'phone',
            'email',
            'description',
            'category',
            'picture',
        )

    def clean(self):
        first_name = self.cleaned_data.get('first_name').strip()
        last_name = self.cleaned_data.get('last_name').strip()

        if first_name.lower() == last_name.lower():
            msg = ValidationError(
                'First name cannot be the same as last name',
                code='invalid'
            )
            self.add_error('last_name', msg)
            self.add_error('first_name', msg)

        return super().clean()

    def clean_first_name(self):
        cleaned_data = self.cleaned_data.get('first_name').strip()

        if cleaned_data.lower() == 'abc' or len(cleaned_data) < 3:
            self.add_error(
                'first_name',
                ValidationError(
                    'Invalid Name',
                    code='invalid'
                )
            )

        return cleaned_data

    def clean_last_name(self):
        cleaned_data = self.cleaned_data.get('last_name').strip()

        if cleaned_data.lower() == 'abc' or len(cleaned_data) < 3:
            self.add_error(
                'last_name',
                ValidationError(
                    'Invalid Name',
                    code='invalid'
                )
            )

        return cleaned_data


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3
    )
    last_name = forms.CharField(
        required=True,
        min_length=3
    )
    email = forms.EmailField(
        required=True
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('E-mail já existente', code='invalid')
            )

        return email
