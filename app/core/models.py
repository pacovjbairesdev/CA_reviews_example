from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                       PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    """Manager for custom user profiles and encrypted passwords"""

    def create_user(self, email, password, **extra_fields):
        """Creates and saves a new user with encrypted password"""
        if not email or email == '':
            raise ValueError('User must have an email address!')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user with encrypted password"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user models that supports email instead of username"""
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Review(models.Model):
    """Tag to be used for a recipe"""
    title = models.CharField(max_length=64)
    rating = models.IntegerField(
            validators=[MaxValueValidator(5), MinValueValidator(1)]
            )
    summary = models.TextField(max_length=10000)
    ip = models.CharField(max_length=45)
    submission_date = models.DateTimeField(auto_now_add=True)
    company = models.CharField(max_length=255)
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title
