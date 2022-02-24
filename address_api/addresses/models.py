from django.db import models
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        For some reason, this doesn't work when I try and create a super user... I am not sure why because
        I thought that I can add the superuser credentials via extra_fields.setdefault('is_superuser', True) ?
        Also tried to use .is_admin and .is_staff but this didn't work either..
        """
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        account = self._create_user(email, password, **extra_fields)
        account.is_admin = True
        account.is_staff = True
        account.save()

        return account


class User(AbstractBaseUser, PermissionsMixin):
    """
    Creating a user using AbstractBaseUser and UserManager (defined above).
    Here, I am making the username the email.
    """

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    password = models.CharField(_('password'), max_length=30)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Return the full name of the user, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_first_name(self):
        """
        Return only the first name of the user.
        """
        return self.first_name


class Address(models.Model):
    """
    Address_line_1, country, and postcode are required fields, address_line_2 and city_or_town
    are not required, and user must be an authorized user.

    In order to address the question of users being unable to add duplicated addresses, I thought adding
    Unique=True to address_line_1 kwargs would be useful. I am assuming that users may have two addresses
    in the same country, with the same postcode and city/town (like a landlord may have). I am also assuming
    that the error is only raised when the input for address_line_1 is EXACTLY the same as inputted before,
    therefore it can be bypassed by changing character case. This should be changed.
    Example:
        There cannot be two addresses with address_line_1 as '86 Worrall Road' however
        '86 worrall Road' will be allowed (bug)
    """
    address_line_1 = models.CharField(max_length=255, unique=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city_or_town = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

