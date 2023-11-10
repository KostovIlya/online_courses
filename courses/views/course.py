from datetime import datetime

import pytz
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from courses.models import Course
from courses.pagination import CoursesLessonsPaginator
from courses.permissions import IsNotModerator, IsOwner
from courses.serializers.course import CourseSerializer
from courses.tasks import send_update_course_email


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CoursesLessonsPaginator

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(owner=self.request.user)

    def perform_update(self, serializer):
        update_course = serializer.save()
        send_update_course_email.delay(update_course.id, update_course.title, update_course.updated_at)
        update_course.updated_at = datetime.now(pytz.timezone('Europe/Moscow'))
        update_course.save()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


