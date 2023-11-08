import stripe
from django.conf import settings
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from courses.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    status = SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'

    def get_status(self, instance):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        payment_intent = stripe.PaymentIntent.retrieve(instance.client_secret)
        return payment_intent.status
