# -*- coding: utf-8 -*-
import arrow
from django.db import models
from products.models import Purchase
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone


# Create your models here.
class AccountUserManager(UserManager):
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, first_name="Default", last_name="Default", **extra_fields):
        """
        Create and save a User with the given details. Default values given to allows create superuser in terminal.
        """

        first_name = email
        last_name = email
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
        """ Extra fields to the User model """

        company = models.CharField(max_length=100, default='')
        objects = AccountUserManager()

        def is_customer(self):
            """ Define if User is a customer by checking if it has any active license """
            try:
                purchases = Purchase.objects.filter(user_id=self.id)
            except Exception:
                return False

            for purchase in purchases:
                if purchase.license_end > arrow.now():
                    return True

            return False
