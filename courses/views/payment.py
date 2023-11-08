import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.models import Payment
from courses.permissions import IsOwner
from courses.serializers.payment import PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    filterset_fields = ['course', 'lesson', 'payment_method']
    # search_fields = ['payment_method']
    ordering_fields = ['payment_date']
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Создание платежа через Stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        payment_intent = stripe.PaymentIntent.create(
            amount=validated_data['payment_amount'],
            currency='usd',
            description=f'Оплата за: {validated_data["course"].title if validated_data["course"] else validated_data["lesson"].title}',
            automatic_payment_methods={"enabled": True},
        )

        validated_data['client_secret'] = payment_intent.id

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response({'client_secret': payment_intent.client_secret}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
