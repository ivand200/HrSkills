from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, Group
from django.utils.translation import gettext_lazy as _
# Create your models here.


class ForceUserManager(UserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_user(self, username, email, password):
    #     client = self._create_user(username, email, password)
    #     #client_group, _ = Group.objects.get_or_create(name="Clients")
    #     #client_group.user_set.add(client)
    #     #client_group.save()
    #     return client

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_default', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, max_length=255)

    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = ForceUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

