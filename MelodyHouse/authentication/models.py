from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, _user_has_perm, _user_get_all_permissions)
from django.db import models

_GENDER = (
    ('F', 'Female'),
    ('M', 'Male'),
    ('O', 'Other'),
    ('*', 'Not to say'),
)

_FAV_GENRES = (
    ('Rock', 'Rock'),
    ('Metal', 'Metal'),
    ('Romantic', 'Romantic'),
    ('Heavy Metal', 'Heavy Metal'),
    ('Jazz', 'Jazz'),
    ('Folk', 'Folk'),
    ('Rap', "Rap"),
)


class UserManager(BaseUserManager):
    def create_user(self, name, phone, email, gender, fav_genre,  password=None, is_staff=False, is_superuser=False):
        if not name or not email or not phone:
            raise ValueError('name, email, phone required')

        if not password:
            raise ValueError('password required')

        user = self.model(name=name, phone=phone, email=email, gender=gender, fav_genre=fav_genre)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, name, phone, email, gender, fav_genre, password=None):
        user = self.create_user(name, phone, email, gender, fav_genre, password, True, False)
        return user

    def create_superuser(self, name, phone, email, gender, fav_genre, password=None):
        user = self.create_user(name, phone, email, gender, fav_genre, password, True, True)


class Account(AbstractBaseUser, PermissionsMixin):
    """
    Doc here
    """
    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=16, unique=True)
    email = models.EmailField(max_length=45, unique=True)
    gender = models.CharField(max_length=1, choices=_GENDER)
    fav_genre = models.CharField(max_length=50, choices=_FAV_GENRES)
    # image = models.ImageField(upload_to='image/user/', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    objects = UserManager()

    def __str__(self):
        return self.name + ': ' + self.phone

    def get_username(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        return False

    def has_module_perm(self, app_label):
        if self.is_superuser:
            return True
        return False

    def has_module_perms(self, perms, obj=None):
        return all(self.has_perm(perm, obj) for perm in perms)
