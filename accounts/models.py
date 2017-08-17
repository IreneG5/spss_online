# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone

industries=(
    ('academic', 'Academic'),
    ('commercial', 'Commercial'),
    ('public-sector', 'Public Sector'),
    ('healthcare', 'Healthcare'),
    ('non-profit', 'Non-profit'),
    ('other', 'Other'),
)


# Create your models here.
class AccountUserManager(UserManager):
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, first_name, last_name, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The username must be set')

        email = self.normalize_email(email)
        user = self.model(username=email, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractUser):
        # with the abstract we can add custom attributes

        company = models.CharField(max_length=100, default='')
        phone = models.CharField(max_length=20, default='')
        industry = models.CharField(max_length=25, choices=industries, default='')

        objects = AccountUserManager()
