from posixpath import basename
from hr.views import FieldViewSet, TagViewSet, ClientViewSet, ClientTag, ManagerViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = "hr"
router = DefaultRouter()


router.register("fields", FieldViewSet, basename="field")
router.register("tags", TagViewSet, basename="tag")
router.register("client", ClientViewSet, basename="client")
router.register("manager", ManagerViewSet, basename="manager")
urlpatterns = router.urls + [
    path("tagsclient/<int:pk>/", ClientTag.as_view()),
]