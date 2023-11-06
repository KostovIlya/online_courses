from rest_framework import serializers

from courses.models import Course, Subscription
from courses.serializers.lesson import LessonSerializer
from courses.validators import DescriptionUrlValidator


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons_1 = LessonSerializer(read_only=True, many=True, source='lessons')
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        validators = [DescriptionUrlValidator(field='description')]

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    def get_is_subscribed(self, instance):
        user = self.context['request'].user
        return Subscription.objects.filter(owner=user, course=instance).exists()
