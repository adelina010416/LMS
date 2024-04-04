from django.db import models

from constants import nullable
from materials.models import Course, Lesson
from users.models import User


class Payment(models.Model):
    PAYMENT_CHOICES = (('cash', 'наличные'), ('transfer', 'перевод'))

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **nullable, verbose_name='курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **nullable, verbose_name='урок')

    date = models.DateTimeField(verbose_name='дата оплаты')
    payment_amount = models.IntegerField(verbose_name='размер платежа')
    payment_way = models.CharField(max_length=10, choices=PAYMENT_CHOICES,
                                   default='transfer', verbose_name='способ оплаты')
