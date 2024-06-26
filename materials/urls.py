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
    path('lessons/detail/<int:pk>', LessonRetrieve.as_view(), name='lesson_detail'),
    path('lessons/update/<int:pk>', LessonUpdate.as_view(), name='lesson_update'),
    path('lessons/delete/<int:pk>', LessonDestroy.as_view(), name='lesson_delete'),
    path('subscribe/', SetSubscription.as_view(), name='subscribe_settings'),
    path('payment/all/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('info/', info, name='info')

              ] + router.urls
