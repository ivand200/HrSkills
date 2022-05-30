from django.test import TestCase
from hr.models import Field, Tag
from rest_framework.test import APIClient, APITestCase, RequestsClient
from rest_framework import status
import json
import requests
import pytest

# Create your tests here.

client = RequestsClient()


def test_create_delete_tag():
    """
    Request for create and delete tag
    """
    payload = {
        "field": 3,
        "title": "footbal"
    }

    request = requests.post("http://127.0.0.1:8000/api/v1/tags/", json=payload)
    request_body = request.json()
    pk = request_body["id"]

    assert request.status_code == 201
    assert request_body["title"] == "footbal"
    assert request_body["field"] == 3

    request_delete = requests.delete(f"http://127.0.0.1:8000/api/v1/tags/{pk}/")

    assert request.status_code == 201


test_data_for_tag = [
    (1, "languages", "English"),
    (4, "skills", "python"),
    (7, "hobbies", "music")
]

@pytest.mark.parametrize("tag_id, field, tag", test_data_for_tag)
def test_get_tag_with_field(tag_id, field, tag):
    """
    Request tag with field by tag.id
    """
    request = requests.get(f"http://127.0.0.1:8000/api/v1/tags/{tag_id}/")
    request_body = request.json()

    assert request.status_code == 200
    assert request_body["field"] == field
    assert request_body["title"] == tag

    pass


def test_get_all_tags():
    """
    Request to get all tags with fields
    """
    request = requests.get("http://127.0.0.1:8000/api/v1/tags/")
    request_body = request.json()

    assert request.status_code == 200
    assert len(request_body["tags"]) > 1



@pytest.mark.django_db
def test_get_fields():
    """
    Get list of all fields
    """
    request = requests.get("http://127.0.0.1:8000/api/v1/fields/")
    request_body = request.json()

    assert request.status_code == 200
    assert len(request_body["fields"]) > 1


test_data_fields = [
    (1, 1),
    (2, 2),
    (3, 3)
]
@pytest.mark.parametrize("field_id, tag_field_id", test_data_fields)
def test_get_field_with_all_tags(field_id, tag_field_id):
    """
    Get field with tags
    """
    request = requests.get(f"http://127.0.0.1:8000/api/v1/fields/{field_id}")
    request_body = request.json()

    assert request.status_code == 200
    assert len(request_body) >= 3
    assert request_body[0]["field"] == tag_field_id


# @pytest.mark.django_db
# def test_create_tag():
#     field = Field.objects.filter(pk=3)
#     print(field)
#     tag = Tag(title="sleep", field=field)
#     tag.save()
#     assert tag.title == "sleep"
#     # assert tag.field_id == 3

