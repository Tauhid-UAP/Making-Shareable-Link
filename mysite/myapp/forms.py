from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import MyUser

from django.contrib.auth import authenticate

class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = (
            'email',
            'password',
        )

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Invalid login.')

class MyUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address.')

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2',)