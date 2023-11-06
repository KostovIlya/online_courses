from rest_framework import serializers

from courses.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'

    def validate(self, attrs):
        user = self.context['request'].user
        course = attrs.get('course')
        if Subscription.objects.filter(owner=user, course=course).exists():
            raise serializers.ValidationError("Вы уже подписаны на этот курс.")
        return attrs
