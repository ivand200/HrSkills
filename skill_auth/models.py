from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, Group
# Create your models here.


class ForceUserManager(UserManager):
    def create_user(self, username, email, password):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_user(self, username, email, password):
    #     client = self._create_user(username, email, password)
    #     #client_group, _ = Group.objects.get_or_create(name="Clients")
    #     #client_group.user_set.add(client)
    #     #client_group.save()
    #     return client

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email and password
        """
        super_user = self._create_user(username, email, password)
        super_user.staff = True
        super_user.admin = True
        super_user.save(using=self._db)
        return super_user


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

