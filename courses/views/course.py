from rest_framework.viewsets import ModelViewSet

from courses.models import Course
from courses.serializers.course import CourseSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
