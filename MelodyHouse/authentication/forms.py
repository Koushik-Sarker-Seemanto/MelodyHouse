from django import forms
from django.contrib.auth import authenticate
from authentication.models import Account
from django.core.exceptions import ObjectDoesNotExist


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs=
                                                          {'placeholder': 'Password (min 6 length)', 'class':
                                                              'form-control', 'minLength': '6', 'maxLength': '12'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs=
                                                                  {'placeholder': 'Confirm Password', 'class':
                                                                      'form-control'}))

    class Meta:
        model = Account
        fields = ['name', 'phone', 'email', 'gender', 'fav_genre']

    widgets = {
        'name': forms.TextInput(attrs={'class':'form-control'}),
        'phone': forms.TextInput(attrs={'class':'form-control'}),
        'email': forms.EmailInput(attrs={'class':'form-control'}),
        'gender': forms.Select(attrs={'class':'custom-select'}),
        'fav_genre': forms.Select(attrs={'class':'custom-select'})
        # 'image': forms.FileInput(attrs={'class':'form-control'})
    }

    def phone(self):
        phone = self.cleaned_data['phone']
        query = Account.objects.filter(phone=phone)
        if query.exists():
            raise forms.ValidationError('phone already registered')
        return phone

    def email(self):
        email = self.cleaned_data['email']
        query = Account.objects.filter(email=email)
        if query.exists():
            raise forms.ValidationError('email already registered')

        return email

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if len(password) < 6:
            raise forms.ValidationError('password should be at least 6 length')
        if len(password) > 12:
            raise forms.ValidationError('password should be at most 12 length')
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('password must contain at least 1 digit')
        if not any(char.isupper() for char in password):
            raise forms.ValidationError('password must contain at least 1 upper letter')
        if not any(char.islower() for char in password):
            raise forms.ValidationError('password must contain at least 1 upper letter')
        if not any(symbol in password for symbol in ['~','!','#','$']):
            raise forms.ValidationError("use any of '~','!','#','$'")
        if not password or not confirm_password or password != confirm_password:
            raise forms.ValidationError('passwords are not matched')
        return confirm_password

    def save(self, commit=True):
        user = Account(
            phone=self.cleaned_data['phone'],
            email=self.cleaned_data['email'],
            gender=self.cleaned_data['gender'],
            name=self.cleaned_data['name'],
            fav_genre=self.cleaned_data['fav_genre'],
            # image=self.cleaned_data['image'],
        )
        user.set_password(self.cleaned_data['confirm_password'])
        if commit:
            user.save()
        return user


class SigninForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data['email']
        password = cleaned_data['password']


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs=
        {'placeholder' : 'Current Password', 'class' : 'form-control'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs=
        {'placeholder' : 'New Password', 'class' : 'form-control', 'minLength':'6'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs=
        {'placeholder' : 'Confirm Password', 'class' : 'form-control'}))

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        isvalid = self.user.check_password(current_password)
        if not isvalid:
            raise forms.ValidationError('invalid password')
        return current_password

    def clean_confirm_password(self):
        password = self.cleaned_data['new_password']
        confirm_password = self.cleaned_data['confirm_password']
        if len(password) < 6:
            raise forms.ValidationError('password should be at least 6 length')
        if len(password) > 12:
            raise forms.ValidationError('password should be at most 12 length')
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('password must contain at least 1 digit')
        if not any(char.isupper() for char in password):
            raise forms.ValidationError('password must contain at least 1 upper letter')
        if not any(char.islower() for char in password):
            raise forms.ValidationError('password must contain at least 1 upper letter')
        if not any(symbol in password for symbol in ['~','!','#','$']):
            raise forms.ValidationError("use any of '~','!','#','$'")
        if not password or not confirm_password or password != confirm_password:
            raise forms.ValidationError('passwords are not matched')
        return confirm_password

    def save(self, commit=True):
        new_password = self.cleaned_data['confirm_password']
        self.user.set_password(new_password)
        if commit:
            self.user.save()
        return self.user

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
