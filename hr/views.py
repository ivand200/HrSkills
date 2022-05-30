# TODO: get all tags by field
# TODO: get all fields
# TODO: get client with all tags group by fields

from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.contrib.auth.models import Group, UserManager, User
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from hr.models import Client, ManagerHR, Tag, Field
from hr.serializers import (
    UserSerializer,
    TagFieldSerializer,
    TagSerializer,
    FieldSerializer,
    ClientTagsSerializer,
    ClientTagFieldSerializer,
    ClientUpdateTagsSerializer
)


# Create your views here.


class TagViewSet(viewsets.ViewSet):
    """
    Manage Tags
    """
    def list(self, request):
        """
        Get all tags with fields
        """
        queryset = Tag.objects.all()
        serializer = TagFieldSerializer(queryset, many=True)
        return JsonResponse({"tags": serializer.data})

    def retrieve(self, request, pk=None):
        """
        Get tag with field by tag.id
        """
        queryset = Tag.objects.all()
        tag = get_object_or_404(queryset, pk=pk)
        serializer = TagFieldSerializer(tag)
        return Response(serializer.data)
        pass

    def create(self, request):
        """
        Create a tag
        """
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Delete tag by id
        """
        queryset = Tag.objects.all()
        tag = get_object_or_404(queryset, pk=pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FieldViewSet(viewsets.ViewSet):
    """
    Manage Fields
    """
    def list(self, request):
        """
        Get all fields
        """
        fields = Field.objects.all()
        serializer = FieldSerializer(fields, many=True)
        return JsonResponse({"fields": serializer.data})

    def retrieve(self, request, pk=None):
        """
        Get tags by field
        """
        queryset = Field.objects.all()
        queryset = Tag.objects.all()
        field = get_object_or_404(queryset, pk=pk)
        tags = Tag.objects.filter(field_id=field.id)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = FieldSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Delete Field
        """
        pass


class ClientViewSet(viewsets.ViewSet):
    """
    Manage Clients
    """

    def retrieve(self, request, pk=None):
        queryset = Client.objects.all()
        client = get_object_or_404(queryset, pk=pk)
        serializer = ClientTagFieldSerializer(client)
        # tags_serializer = Tag.objects.
        return Response(serializer.data)

        # queryset = Client.objects.all()
        # client = get_object_or_404(queryset, pk=pk)
        # serializer = ClientTagsSerializer(client)
        # return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        # return Response(serializer.initial_data)
        if serializer.is_valid():
            new_client = serializer.save()
            client_group, _ = Group.objects.get_or_create(name="Clients")
            client_group.user_set.add(new_client)
            client_group.save()
            client = Client(user=new_client)
            client.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Update Client
        """
        # queryset = Client.objects.all()
        # client = get_object_or_404(queryset, pk=pk)
        # serializer = ClientTagFieldSerializer(client, data=request.data)
        # if serializer.is_valid(raise_exception=True):
        #     return Response(serializer.data)
        # return Response("False")
        # # serializer = ClientTagFieldSerializer(data=client)
        # # if serializer.is_valid(raise_exception=True):
        # #     return Response(serializer.data)
        # # return Response("False")
    
    @action(detail=True, methods=["put"])
    def update_tags(self, request, pk=None):
        """
        Add tags to client
        """
        queryset = Client.objects.all()
        client = get_object_or_404(queryset, pk=pk)
        tags = request.data["tags_id"]
        for item in tags:
            client.tag.add(item)
        return Response(
            f"{tags} was added to client {client.user.email}",
            status=status.HTTP_200_OK
        )

        # queryset = Client.objects.all()
        # client = get_object_or_404(queryset, pk=pk)
        # tags = request.data["tags_id"]
        # tags_objects = Tag.objects.filter(id__in=tags)
        # client.tag.set(tags_objects)
        # # for item in tags_objects:
        # #     client.tag.set(item)
        # return Response(f"{tags} was added", status=status.HTTP_200_OK)

        # serializer = ClientUpdateTagsSerializer(client, data={"tag": tags}, partial=True)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # tags_objects = Tag.objects.filter(id__in=tags)
        # for item in tags_objects:
        #     client.tag.add(item)

    @action(detail=True, methods=["delete"])
    def delete_tags(self, request, pk=None):
        """
        Delete tags from client
        """
        queryset = Client.objects.all()
        client = get_object_or_404(queryset, pk=pk)
        tags = request.data["tags_id"]
        for item in tags:
            client.tag.remove(item)
        return Response(
            f"tags: {tags} was removed from user: {client.user.email}",
            status=status.HTTP_200_OK
        )


class ManagerViewSet(viewsets.ViewSet):
    """
    Manager create, delete, update
    """
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_manager = serializer.save()
            manager_group, _ = Group.objects.get_or_create(name="Managers")
            manager_group.user_set.add(new_manager)
            manager_group.save()
            manager = ManagerHR(user=new_manager)
            manager.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientTag(APIView):
    """
    add, updatedelete clients tags
    """
    def _get_client(self, pk):
        client = get_object_or_404(Client, pk=pk)
        return client

    def post(self, request, pk=None):
        client = self._get_client(pk)
        tags = request.data["tags"]
        tags_objects = Tag.objects.filter(id__in=tags)
        for item in tags_objects:
            client.tag.add(item)
        return Response("Check")

    def get(self, request, pk=None):
        pass
        # client = self._get_client(pk)
        # serializer = ClientTagsSerializer(client)
        # return Response(serializer.data)
