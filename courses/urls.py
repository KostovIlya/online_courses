from django.urls import path
from rest_framework.routers import DefaultRouter

from courses.apps import CoursesConfig
from courses.views.course import CourseViewSet
from courses.views.lesson import LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonDestroyAPIView, \
    LessonUpdateAPIView
from courses.views.payment import PaymentListAPIView
from courses.views.subscription import SubscriptionCreateAPIView, SubscriptionDestroyAPIView

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

    path('course/payment/', PaymentListAPIView.as_view(), name='payments'),

    path('subscription/', SubscriptionCreateAPIView.as_view(), name='subscription'),
    path('subscription/<int:pk>/delete/', SubscriptionDestroyAPIView.as_view(), name='subscription_delete'),
] + router.urls
