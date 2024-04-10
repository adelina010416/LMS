import stripe
from celery import shared_task
from django.core.mail import send_mail
from stripe import InvalidRequestError

from config import settings
from materials.models import Subscription, Lesson

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_session(payment, title):
    """ Получает сессию для оплаты курса """
    product = stripe.Product.create(name=title)
    price = stripe.Price.create(
        unit_amount=payment.payment_amount * 100,
        currency='rub',
        product=product.id,
    )
    session = stripe.checkout.Session.create(
        success_url='http://localhost:8000/info',
        line_items=[
            {
                'price': price.id,
                'quantity': 1,
            }
        ],
        mode='payment',
        customer_email=payment.user.email
    )
    return session


def get_payment_status(payments):
    for payment in payments:
        try:
            session = stripe.checkout.Session.retrieve(payment.session_id, )
            payment.status = session.payment_status
            payment.save()
        except InvalidRequestError:
            continue


@shared_task
def send_course_notification(obj_id, obj_type, action=None):
    if obj_type == 'course':
        subscriptions = Subscription.objects.filter(course=obj_id)
        subject = 'Обновление курса'
        message = f'Детали курса "{subscriptions.first().course.name}" были обновлены.'
    else:
        lesson = Lesson.objects.filter(pk=obj_id).first()
        subscriptions = Subscription.objects.filter(course=lesson.course.id)
        if action == 'create':
            subject = 'Доступен новый урок'
            message = f'На курс "{subscriptions.first().course.name}" добавлен новый урок "{lesson.name}".'
        else:
            subject = 'Обновление урока'
            message = f'Детали урока "{lesson.name}" с курса "{lesson.course.name}" были обновлены.'
    if subscriptions.exists():
        for subscription in subscriptions:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscription.user.email],
            )


# @shared_task
# def send_update_course_notification():
#     pass
