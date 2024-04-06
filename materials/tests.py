from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson, Course, Subscription
from users.models import User


class LessonsAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru', is_active=True, is_staff=False)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='test_course', author=self.user)
        self.lesson = Lesson.objects.create(
            name='test_lesson',
            course=self.course,
        )

    def test_lesson_list(self):
        """ Проверка списка уроков """
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(),
                         {'detail': 'У вас недостаточно прав для выполнения данного действия.'})
        moderator = User.objects.create(email='testmoderator@mail.ru', is_active=True, is_staff=True)
        self.user.set_password('test_m_password')
        self.user.save()
        self.client.force_authenticate(user=moderator)
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'count': 1,
                          'next': None,
                          'previous': None,
                          'results':
                              [
                                  {'id': self.lesson.id, 'name': self.lesson.name,
                                   'description': self.lesson.description, 'preview': None,
                                   'link_video': self.lesson.link_video, 'course': self.lesson.course.id}
                              ]
                          })

    def test_lesson_retrieve(self):
        """ Проверка получения урока """
        response = self.client.get(f'/lessons/detail/{self.lesson.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'id': self.lesson.id,
                          'name': self.lesson.name,
                          'description': self.lesson.description,
                          'preview': self.lesson.preview,
                          'link_video': self.lesson.link_video,
                          'course': self.lesson.course.id,
                          }
                         )

    def test_lesson_create(self):
        """ Проверка создания урока """
        data_without_link = {
            "name": "test2",
            "description": '',
            "preview": '',
            "link_video": '',
            "course": 1
        }
        data_valid_link = {
            "name": "test2",
            "description": '',
            "preview": '',
            "link_video": 'youtube.com/sgdjhgaskd',
            "course": 1
        }
        data_invalid_link = {
            "name": "test2",
            "description": '',
            "preview": '',
            "link_video": 'pornhub.com',
            "course": 1
        }
        response = self.client.post('/lessons/create/', data=data_without_link)
        valid_response = self.client.post('/lessons/create/', data=data_valid_link)
        invalid_response = self.client.post('/lessons/create/', data=data_invalid_link)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(valid_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(invalid_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(invalid_response.json(),
                         {'non_field_errors': ['You can only attach links to videos on YouTube.']})
        self.assertEqual(Lesson.objects.count(), 3)

    def test_lesson_update(self):
        """ Проверка обновления урока """
        data = {
            'name': 'test_change',
            'description': 'big change',
            'preview': '',
            'link_video': '',
            'course': self.course.id
        }
        response = self.client.put(f'/lessons/update/{self.lesson.id}', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'id': self.lesson.id,
                          'name': data['name'],
                          'description': data['description'],
                          'preview': None,
                          'link_video': data['link_video'],
                          'course': data['course']
                          }
                         )

    def test_lesson_delete(self):
        """ Проверка удаления урока """
        response = self.client.delete(f'/lessons/delete/{self.lesson.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru', is_active=True)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='test525', author=self.user)
        self.lesson = Lesson.objects.create(
            name='test_lesson',
            description='very_interesting_test',
            course=self.course,
        )
        self.data = {"id": self.course.id}

    def test_set_subscription(self):
        """ Проверка добавления подписки """
        response = self.client.post('/subscribe/', self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "подписка добавлена"})
        self.assertEqual(Subscription.objects.count(), 1)

        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
        )
        response = self.client.post('/subscribe/', self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "подписка удалена"})
        self.assertEqual(Subscription.objects.count(), 0)
