# from rest_framework import status
# from rest_framework.test import APITestCase
#
# from materials.models import *
# from users.models import User
#
#
# class SubscriptionAPITestCase(APITestCase):
#     def setUp(self):
#         self.data = {'id': 1}
#         self.user = User.objects.create(email='test@mail.ru', is_active=True)
#         self.user.set_password('test_password')
#         self.user.save()
#         self.client.force_authenticate(user=self.user)
#         self.course = Course.objects.create(name='test525', author=self.user)
#         self.lesson = Lesson.objects.create(
#             name='test_lesson',
#             description='very_interesting_test',
#             course=self.course,
#         )
#
#     def test_set_subscription(self):
#         """ Проверка добавления подписки """
#         response = self.client.post('/subscribe/', self.data)
#         print(response.status_code)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.json(), {"message": "подписка добавлена"})
#         self.assertEqual(Subscription.objects.count(), 1)
#
#         self.subscription = Subscription.objects.create(
#             user=self.user,
#             course=self.course,
#         )
#         response = self.client.post('/subscribe/', self.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.json(), {"message": "подписка удалена"})
#         self.assertEqual(Subscription.objects.count(), 0)