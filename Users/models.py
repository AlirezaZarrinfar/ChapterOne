import datetime
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password):
        if not email:
            raise ValueError('user must have email')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.full_name = full_name
        user.role = USER_ROLE
        user.save()
        return user

    def create_superuser(self, email, password, full_name):
        user = self.create_user(email, full_name, password)
        user.role = ADMIN_ROLE
        user.save()
        return user


ADMIN_ROLE = 1
USER_ROLE = 2


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    role = models.IntegerField()
    date_joined = models.DateTimeField(default=datetime.datetime.now())

    REQUIRED_FIELDS = ['full_name']

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.full_name

    def has_module_perms(user_obj, app_label):
        return True

    def has_perm(perm, obj=None):
        return True

    @property
    def is_staff(self):
        return self.role == ADMIN_ROLE
