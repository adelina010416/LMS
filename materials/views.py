from datetime import datetime

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, serializers
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from materials.models import Course, Lesson, Subscription, Payment
from materials.paginators import MyPagination
from materials.permissions import IsNotStaffUser, IsOwner, IsModarator, IsCustomer
from materials.serializer import CourseSerializer, LessonSerializer, SubscriptionSerializer, PaymentSerializer
from materials.services import get_session, get_payment_status, send_course_notification


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MyPagination

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsNotStaffUser & IsAuthenticated]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            user_payments = Payment.objects.filter(user=self.request.user, status='unpaid')
            get_payment_status(user_payments)
            permission_classes = [IsAuthenticated & (IsModarator | IsOwner | IsCustomer)]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated & (IsModarator | IsOwner)]
        elif self.action == 'destroy':
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save(author=self.request.user).id
        send_course_notification.delay(obj_id=course, obj_type='course')


class LessonList(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & IsModarator]
    pagination_class = MyPagination


class LessonCreate(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsNotStaffUser & IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.save()
        user_courses = Course.objects.filter(author=self.request.user)
        if lesson.course not in user_courses:
            raise serializers.ValidationError('Курс не найден. Пожалуйста, укажите один из своих курсов.')
        send_course_notification.delay(lesson.id, 'lesson', 'create')


class LessonRetrieve(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & (IsModarator | IsOwner | IsCustomer)]

    def refresh_status(self):
        user_payments = Payment.objects.filter(user=self.request.user, status='unpaid')
        get_payment_status(user_payments)


class LessonUpdate(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & (IsModarator | IsOwner)]

    def perform_update(self, serializer):
        lesson = serializer.save()
        user_courses = Course.objects.filter(author=self.request.user)
        if lesson.course not in user_courses:
            raise serializers.ValidationError('Курс не найден. Пожалуйста, укажите один из своих курсов.')
        send_course_notification.delay(lesson.id, 'lesson', action='update')


class LessonDestroy(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & IsOwner]


class SetSubscription(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('id')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'
        return Response({"message": message})


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('payment_way', 'course', 'lesson',)
    ordering_fields = ('date',)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_payments = Payment.objects.filter(user=self.request.user, status='unpaid')
        get_payment_status(user_payments)
        return Payment.objects.filter(user=self.request.user)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        course = self.request.data.get('course')
        lesson = self.request.data.get('lesson')
        payment_way = self.request.data.get('payment_way')
        if not course and not lesson:
            raise serializers.ValidationError('Пожалуйста, укажите или курс, или урок, который хотели бы приобрести.')
        if course and lesson:
            raise serializers.ValidationError('Пожалуйста, выберите что-то одно: курс или урок.')
        if not payment_way:
            payment_way = 'transfer'
        if course:
            course_data = get_object_or_404(Course, pk=course)
            paid_course = Payment.objects.filter(user=self.request.user, course=course, status='paid')
            if paid_course.exists():
                raise serializers.ValidationError(f'Курс "{course_data.name}" уже оплачен.')
            else:
                payment = Payment.objects.create(payment_way=payment_way,
                                                 user=self.request.user,
                                                 date=datetime.now(),
                                                 course=course_data,
                                                 payment_amount=course_data.price)
                purchase_name = f'Курс {course_data.name}'
        else:
            lesson_data = get_object_or_404(Lesson, pk=lesson)
            paid_lesson = Payment.objects.filter(user=self.request.user, lesson=lesson, status='paid')
            if paid_lesson.exists():
                raise serializers.ValidationError(f'Урок "{lesson_data.name}" уже оплачен.')
            else:
                payment = Payment.objects.create(payment_way=payment_way,
                                                 user=self.request.user,
                                                 date=datetime.now(),
                                                 lesson=lesson_data,
                                                 payment_amount=lesson_data.price)
                purchase_name = f'Урок {lesson_data.name}'
        if payment.payment_way == 'transfer':
            session = get_session(payment, purchase_name)
        link = session.url
        payment.session_id = session.id
        payment.save()
        return Response({"message": f'Для оплаты перейдите по ссылке: {link}'})


@api_view(['GET'])
def info(request):
    context = {'header': 'Успешно!', 'body': 'Оплата прошла успешно, можете закрыть страницу.'}
    return Response(context)
