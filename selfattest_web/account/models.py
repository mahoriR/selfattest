import time
import uuid

from django.db import models
from django.db.models import F
from common.constants import Length
from common.uuid import unique_uuid4
from common.abstract_models import AbstractExternalFacing, AbstractTimeStamped, AbstractVersioned

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class SelfattestUserManager(BaseUserManager):

    def create_user(self, email: str, password: str = None) -> 'SelfattestUser':
        """
        Creates and saves a User with the given email, and password.
        """
        if not email:
            raise ValueError('Users must have an email')

        user = self.model(email=email)

        password = password or self.make_random_password()

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **kwargs):  # pragma: no cover
        """
        Creates and saves a superuser with the given phone, password.
        """
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class SelfattestUser(AbstractBaseUser, AbstractExternalFacing, AbstractTimeStamped, AbstractVersioned):

    email = models.CharField(
        unique=True, verbose_name='email',
        max_length=Length.EMAIL)

    is_active = models.BooleanField(default=True)  # Part of JWT

    is_suspended = models.BooleanField(default=False)  # Part of JWT

    is_admin = models.BooleanField(default=False)

    objects = SelfattestUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):  # pragma: no cover
        return self.email

    class Meta:
        db_table = 'selfattest_user'
        indexes = [
            models.Index(fields=['email',]),
            models.Index(fields=['external_id']),
        ]

    def has_perm(self, perm, obj=None):  # pragma: no cover
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):  # pragma: no cover
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):  # pragma: no cover
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
