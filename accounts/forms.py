from django import forms
from django.contrib.auth import authenticate
from .models import Account 
from django.contrib import messages


User = Account


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Emails must match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError(
                "This email has already been registered")
        return super(UserRegisterForm, self).clean(*args, **kwargs)


class SendMoneyForm(forms.Form):
    money = forms.FloatField(label='Money to send')
    #Options = [
    #    ('1', 'GEL'),
    #    ('2', 'USD'),
    #    ('3', 'EUR'),
    #  ]
    #selected_card = forms.ChoiceField(label='Card', widget=forms.Select, choices=Options)
    receiver_card = forms.CharField(label='Card ID')

    def clean(self, *args, **kwargs):
        if self.cleaned_data.get('money') <= 0:
            raise forms.ValidationError('Money <= 0')

class AccountUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']