from rest_framework import serializers

from courses.models import Course
from courses.serializers.lesson import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, instance):
        return instance.lessons.count()
