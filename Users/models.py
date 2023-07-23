import datetime
import re

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


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
    rated_books = models.ManyToManyField('SocialMedia.Book', through='SocialMedia.Rating', related_name='books_rated')
    favorite_books = models.ManyToManyField('SocialMedia.Book', through='SocialMedia.FavoriteBook', related_name='books_favorited_by')
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    following_num = models.IntegerField(default=0)
    followers_num = models.IntegerField(default=0)

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

    def validate_password(password):
        if len(password) < 8:
            return False

        if not re.search(r'[A-Z]', password):
            return False

        if not re.search(r'[a-z]', password):
            return False

        return True

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )