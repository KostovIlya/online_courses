from django.core.management import BaseCommand

from courses.models import Payment, Course, Lesson
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(id=1)
        course = Course.objects.get(id=1)
        lesson = Lesson.objects.get(id=2)
        Payment.objects.bulk_create([
            Payment(user=user, course=course, payment_amount=500, payment_method=Payment.PaymentMethod.CASH),
            Payment(user=user, lesson=lesson, payment_amount=600, payment_method=Payment.PaymentMethod.CASH),
            Payment(user=user, course=course, payment_amount=700, payment_method=Payment.PaymentMethod.CASH),
            Payment(user=user, course=lesson, payment_amount=500, payment_method=Payment.PaymentMethod.TRANSFER),
            Payment(user=user, course=course, payment_amount=500, payment_method=Payment.PaymentMethod.TRANSFER)
        ])

