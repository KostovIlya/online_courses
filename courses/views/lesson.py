from datetime import datetime

import pytz
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from courses.models import Lesson
from courses.pagination import CoursesLessonsPaginator
from courses.permissions import IsOwner, IsNotModerator
from courses.serializers.lesson import LessonSerializer
from courses.tasks import send_update_course_email


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CoursesLessonsPaginator

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save(owner=self.request.user)
        send_update_course_email.delay(new_lesson.course.id, new_lesson.course.title,
                                       new_lesson.course.updated_at)
        new_lesson.course.updated_at = datetime.now(pytz.timezone('Europe/Moscow'))
        new_lesson.course.save()


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]

    def perform_update(self, serializer):
        update_lesson = serializer.save()
        send_update_course_email.delay(update_lesson.course.id, update_lesson.course.title,
                                       update_lesson.course.updated_at)
        update_lesson.course.updated_at = datetime.now(pytz.timezone('Europe/Moscow'))
        update_lesson.course.save()


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
