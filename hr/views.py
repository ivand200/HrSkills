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

from hr.models import Client, Tag, Field
from hr.serializers import ClientSerializer, TagFieldSerializer, TagSerializer, FieldSerializer, ClientTagsSerializer, ClientTagFieldSerializer


# Create your views here.


class TagViewSet(viewsets.ViewSet):
    """
    Tags
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
    Fields
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


class ClientViewSet(viewsets.ViewSet):
    """
    Create, Update, Delete Clients
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
        serializer = ClientSerializer(data=request.data)
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
        pass


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
        ClientTagFieldSerializer
        # client = self._get_client(pk)
        # serializer = ClientTagsSerializer(client)
        # return Response(serializer.data)
