from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from datetime import datetime, timedelta


class TeamUserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('user must have an email address.')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class TeamUser(AbstractUser, PermissionsMixin):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    team_name = models.CharField(max_length=100, default='Team Name')
    team_logo = models.ImageField(
        upload_to='media/logos/', blank=True, null=True)
    coach_name = models.CharField(max_length=100, default='John Doe')
    coach_contact = models.CharField(max_length=100, default='0712345678')
    location = models.CharField(max_length=100, default='Nairobi')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = TeamUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
