from dataclasses import field
import email
from enum import unique
from rest_framework import serializers
from .models import Field, Tag, Client, ManagerHR
from django.contrib.auth.models import Group
from skill_auth.models import User


class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Field
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


class TagFieldSerializer(serializers.ModelSerializer):
    field = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="title"
    )
    class Meta:
        model = Tag
        fields = "__all__"


class ClientFullSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email"]


class ClientTagFieldSerializer(serializers.ModelSerializer):
    tag = TagFieldSerializer(read_only=True, many=True)
    user = ClientFullSerializer(read_only=True)

    class Meta:
        model = Client
        fields = ["user", "id", "tag",]


class ClientTagsUpdateSecondSerializer(serializers.ModelSerializer):


    class Meta:
        model = Tag
        fields = ["id"]


class ClientUpdateTagsSerializer(serializers.ModelSerializer):
    tag = ClientTagsUpdateSecondSerializer(many=True)
    # tag = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field="id"
    # )

    class Meta:
        model = Client
        fields = ["tag", "user"]

    def update(self, instance, validated_data):
        instance.tag = validated_data.get("tags", instance.tag)
        instance.save()
        return instance

class ClientTagsSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="title"
    )

    class Meta:
        model = Client
        fields = ["tag", "id"]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        username = self.validated_data["username"]
        email = self.validated_data["email"]
        password = self.validated_data["password"]
        new_client = User.objects.create_user(username=username, email=email, password=password)
        return new_client




