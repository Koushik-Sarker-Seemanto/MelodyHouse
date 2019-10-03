
from django import forms
from django.contrib.auth import authenticate
from authentication.models import Account


class ProfileUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs=
        {'class': 'form-control', 'placeholder' : 'Your Password'}))

    class Meta:
        model = Account
        fields = ['name','phone', 'email', 'gender', 'fav_genre']

        widgets = {
            'name' : forms.TextInput(attrs={
                'placeholder' : 'Name', 'class' : 'form-control'
                }),
            'phone' : forms.TextInput(attrs={
                'placeholder' : 'Phone Number', 'class':'form-control'
                }),

            'email' : forms.EmailInput(attrs={
                'placeholder' : 'Email (optional)', 'class' : 'form-control'
                }),

            'gender': forms.Select(attrs={
                'class': 'custom-select'
                }),
            'fav_genre': forms.Select(attrs={
                'class': 'custom-select'
                }),
        }

    def clean(self):
        cleaned_data = self.cleaned_data

        password = cleaned_data['password']
        phone = cleaned_data['phone']
        email = cleaned_data['email']
        gender = cleaned_data['gender']
        fav_genre = cleaned_data['fav_genre']

        valid = self.user.check_password(password)
        if not valid:
            raise forms.ValidationError('invalid password')

        duplicate_email = Account.objects.filter(email=email).exclude(id=self.user.id)
        if duplicate_email.exists():
            raise forms.ValidationError('This email is already registered')

        duplicate_phone = Account.objects.filter(phone=phone).exclude(id=self.user.id)
        if duplicate_phone.exists():
            raise forms.ValidationError('This phone is already registered')

        if gender is None:
            raise forms.ValidationError('set a gender')
        if fav_genre is None:
            raise forms.ValidationError('Choose favourite Genre')

        return cleaned_data

    def is_new_email(self):
        if self.user.email.lower() != self.cleaned_data.get('email').lower():
            return True
        return False

    def save(self, commit=True):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        gender = self.cleaned_data['gender']
        phone = self.cleaned_data['phone']
        fav_genre = self.cleaned_data['fav_genre']
        self.user.name = name
        self.user.phone = phone
        self.user.email = email
        self.user.gender = gender
        self.user.fav_genre = fav_genre

        if commit:
            self.user.save()
        return self.user

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)

        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        self.fields['name'].initial = self.user.name
        self.fields['phone'].initial = self.user.phone
        self.fields['email'].initial = self.user.email
        self.fields['gender'].initial = self.user.gender
        self.fields['fav_genre'].initial = self.user.fav_genre
