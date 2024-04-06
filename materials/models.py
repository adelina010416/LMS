from django.db import models

from constants import nullable
from users.models import User


# from users.models import User


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(max_length=250, **nullable, verbose_name='описание')
    preview = models.ImageField(upload_to='courses/', **nullable, verbose_name='превью')
    author = models.ForeignKey(User, on_delete=models.CASCADE, **nullable, verbose_name='автор')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(max_length=250, **nullable, verbose_name='описание')
    preview = models.ImageField(upload_to='lessons/', **nullable, verbose_name='превью')
    link_video = models.CharField(max_length=500, **nullable, verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    def __str__(self):
        return f"{self.user}: {self.course}"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
