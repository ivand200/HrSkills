from django.db import models
from django.contrib.auth.models import Group, UserManager, User
from django.conf import settings

# Create your models here.


class Field(models.Model):
    title = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=20, unique=True)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, null=True)
    # tag = models.ForeignKey(Tag, related_name="tags", on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.__class__.__name__} object for {self.user}"


