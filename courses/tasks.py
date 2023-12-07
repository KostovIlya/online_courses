from datetime import datetime, timedelta

import pytz
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from courses.models import Subscription
from users.models import User


@shared_task
def send_update_course_email(course_id, course_title, course_updated_at):
    owner_email_list = [subscription.owner.email for subscription in Subscription.objects.filter(course_id=course_id)]
    current_time = datetime.now(pytz.timezone('Europe/Moscow'))

    if not course_updated_at:
        course_updated_at = current_time

    updated_time = course_updated_at
    time_difference = current_time - updated_time

    if owner_email_list and time_difference >= timedelta(hours=4):
        send_mail(
            subject='Обновление курса',
            message=f'Курс {course_title} обновлен',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=owner_email_list
        )


@shared_task
def last_login_users_check():
    block_list = []
    thirty_days_ago = datetime.now() - timedelta(days=30)
    users = User.objects.filter(last_login__lt=thirty_days_ago)
    for user in users:
        user.is_active = False
        block_list.append(user)

    User.objects.bulk_update(block_list, ['is_active'])
