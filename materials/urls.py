from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import *

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/', LessonList.as_view(), name='lessons'),
    path('lessons/create/', LessonCreate.as_view(), name='lesson_create'),
    path('lessons/detail/<int:pk>', LessonRetrieveUpdate.as_view(), name='lesson_detail_update'),
    path('lessons/delete/<int:pk>', LessonDestroy.as_view(), name='lesson_delete'),
              ] + router.urls
