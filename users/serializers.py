from rest_framework import serializers

from courses.serializers.payment import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'avatar', 'phone', 'city', 'payments')
