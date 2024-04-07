import stripe
from stripe import InvalidRequestError

from config import settings
from materials.models import Payment

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
            session = stripe.checkout.Session.retrieve(payment.session_id,)
            payment.status = session.payment_status
            payment.save()
        except InvalidRequestError:
            continue
