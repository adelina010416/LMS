from django.contrib.auth.models import AbstractUser
from django.db import models

from constants import nullable
from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=250, unique=True, verbose_name='почта')
    phone = models.CharField(max_length=50, unique=True, **nullable, verbose_name='телефон')
    city = models.CharField(max_length=100, **nullable, verbose_name='город')
    avatar = models.ImageField(upload_to='users/', **nullable, verbose_name='аватар')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payment(models.Model):
    PAYMENT_CHOICES = (('cash', 'наличные'), ('transfer', 'перевод'))

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **nullable, verbose_name='курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **nullable, verbose_name='урок')

    date = models.DateTimeField(verbose_name='дата оплаты')
    payment_amount = models.IntegerField(verbose_name='размер платежа')
    payment_way = models.CharField(max_length=10, choices=PAYMENT_CHOICES,
                                   default='transfer', verbose_name='способ оплаты')
