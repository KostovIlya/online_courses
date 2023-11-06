from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from courses.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@test.com',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        self.user.set_password('0000')
        self.user.save()
        self.access_token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.course = Course.objects.create(
            title='test_course',
            description='test_description',
            owner=self.user
        )

        self.lesson = Lesson(title='test_course', description='test_description', course=self.course, owner=self.user)
        self.lesson.save()

    def test_create_lesson(self):
        """Тестирование создания урока"""
        data = {'title': 'test', 'description': 'test_description', 'course': self.course.pk}
        response = self.client.post('/lesson/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], data['title'])
        self.assertEqual(response.json()['course'], self.course.pk)
        self.assertEqual(response.json()['owner'], self.user.pk)
        self.assertEqual(Lesson.objects.filter(id=response.json()['id']).exists(), True)

    def test_list_lessons(self):
        """Тестирование получения списка уроков"""
        lessons = list(Lesson.objects.all())
        response = self.client.get('/lesson/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], len(lessons))
        self.assertEqual(response.json()['results'][0]['id'], lessons[0].pk)

        user_2 = User(email='test33@test.com', is_active=True)
        user_2.set_password('0000')
        user_2.save()
        access_token = str(AccessToken.for_user(user_2))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.get('/lesson/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_lesson(self):
        """Тестирование получения урока"""
        response = self.client.get(f'/lesson/{self.lesson.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.lesson.pk)
        self.assertEqual(response.json()['title'], self.lesson.title)
        self.assertEqual(response.json()['preview'], self.lesson.preview)
        self.assertEqual(response.json()['description'], self.lesson.description)
        self.assertEqual(response.json()['video_link'], self.lesson.video_link)
        self.assertEqual(response.json()['course'], self.lesson.course.pk)
        self.assertEqual(response.json()['owner'], self.lesson.owner.pk)

    def test_update_lesson(self):
        """Тестирование изменения урока"""
        invalid_description = {'title': 'new_test', 'description': 'Какое-то описание https://www.test.com',
                               'course': self.course.pk}
        valid_description = {'title': 'new_test', 'description': 'Какое-то описание https://www.youtube.com/test',
                             'course': self.course.pk}
        no_data = {}

        response = self.client.put(f'/lesson/{self.lesson.pk}/update/', invalid_description)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Недопустимый URL!']})

        response = self.client.put(f'/lesson/{self.lesson.pk}/update/', valid_description)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], valid_description['title'])
        self.assertEqual(response.json()['description'], valid_description['description'])

        response = self.client.put(f'/lesson/{self.lesson.pk}/update/', no_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'course': ['This field is required.'],
                                           'description': ['This field is required.'],
                                           'title': ['This field is required.']})

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        response = self.client.delete(f'/lesson/{self.lesson.pk}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.filter(pk=self.lesson.pk).exists(), False)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@test.com',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        self.user.set_password('0000')
        self.user.save()
        self.access_token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.course = Course.objects.create(
            title='test_course',
            description='test_description',
            owner=self.user
        )
        self.course.save()

    def test_subscription_create(self):
        """Тестирование создания подписки"""
        data = {'course': self.course.pk}
        response = self.client.post('/subscription/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['course'], self.course.pk)
        self.assertEqual(response.json()['owner'], self.user.pk)

        # Повторное создание уже существующей подписки
        response = self.client.post('/subscription/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Вы уже подписаны на этот курс.']})

        # Проверка признака подписки в курсе
        response = self.client.get(f'/course/{self.course.pk}/')
        self.assertEqual(response.json()['is_subscribed'], True)

    def test_subscription_delete(self):
        """Тестирование удаления подписки"""
        self.subscription = Subscription.objects.create(
            owner=self.user,
            course=self.course
        )
        self.subscription.save()
        response = self.client.delete(f'/subscription/{self.subscription.pk}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверка признака подписки в курсе
        response = self.client.get(f'/course/{self.course.pk}/')
        self.assertEqual(response.json()['is_subscribed'], False)

        # Проверка существования подписки в БД
        self.assertEqual(Subscription.objects.filter(pk=response.json()['id']).exists(), False)