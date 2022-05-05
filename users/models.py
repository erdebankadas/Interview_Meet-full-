from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from rest_framework.authtoken.models import Token
import uuid

#Email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
        )
        user.is_admin = True
        user.role = 'ROLE_ADMIN'
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10, unique=True, null=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    token = models.UUIDField(unique=True, default=uuid.uuid4)
    role = models.CharField(max_length=10, default='ROLE_USER')
    auth_provider = models.CharField(max_length=20, default='email')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    extra_fields = models.TextField(null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Hr(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='hr_created',
        null=True
    )

    def __str__(self) -> str:
        return self.user.email



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)