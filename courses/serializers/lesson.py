from rest_framework import serializers

from courses.models import Lesson
from courses.validators import DescriptionUrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [DescriptionUrlValidator(field='description')]
