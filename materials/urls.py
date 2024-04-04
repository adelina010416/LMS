from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import *

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/', LessonList.as_view(), name='lessons'),
    path('lessons/detail/<int:pk>', LessonDetail.as_view(), name='lesson')
              ] + router.urls
