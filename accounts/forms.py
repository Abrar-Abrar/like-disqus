from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Member

User = get_user_model()


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password from numbers and letters of the Latin alphabet'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password confirm'}))

    class Meta:
        model = User
        fields = fields = ("username", "first_name",
                           "last_name", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-Mail'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        exclude = ['user']


class EmailValidationBeforeResetPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if not User.objects.filter(email=email, is_active=True).exists():
            raise ValidationError(
                "There is no user registered with this email address")
        return email
