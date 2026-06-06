"""Formulaires : inscription, connexion, OTP, validation secondaire."""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.conf import settings
from .models import User


class RegisterForm(UserCreationForm):
    accepte_cgu = forms.BooleanField(required=True, label="J'accepte les CGU")
    accepte_confidentialite = forms.BooleanField(required=True, label="J'accepte la Politique de confidentialité")
    accepte_mentions = forms.BooleanField(required=True, label="J'ai pris connaissance des Mentions légales")

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email',
            'nationality', 'date_naissance',
            'password1', 'password2',
        ]
        widgets = {'date_naissance': forms.DateInput(attrs={'type': 'date'})}

    def clean_date_naissance(self):
        date_naissance = self.cleaned_data.get('date_naissance')
        if date_naissance:
            from django.utils import timezone
            age_min = getattr(settings, 'AGE_MINIMUM', 16)
            today = timezone.now().date()
            age = today.year - date_naissance.year
            if today.month < date_naissance.month or (
                today.month == date_naissance.month and today.day < date_naissance.day
            ):
                age -= 1
            if age < age_min:
                raise forms.ValidationError(f'Vous devez avoir au moins {age_min} ans.')
        return date_naissance


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'placeholder': 'vous@exemple.com'})
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'vous@exemple.com'})
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='Nouveau mot de passe',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )
    confirm_password = forms.CharField(
        label='Confirmer',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        cpwd = cleaned_data.get('confirm_password')
        if pwd and cpwd and pwd != cpwd:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return cleaned_data


class OTPForm(forms.Form):
    code = forms.CharField(
        label='Code OTP',
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': 'Code à 6 chiffres',
            'inputmode': 'numeric',
            'autocomplete': 'one-time-code',
            'maxlength': '6',
        })
    )


class ValidationSecondaireForm(forms.Form):
    code_validation = forms.CharField(
        label='Code de validation',
        max_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': 'Code de validation',
            'inputmode': 'numeric',
        })
    )
