from django.contrib.auth import get_user_model
from django.db import models

from users.models import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='courses/preview', verbose_name='превью(картинка)', **NULLABLE)
    description = models.TextField(verbose_name='описание')

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='courses/preview', verbose_name='превью(картинка)', **NULLABLE)
    video_link = models.URLField(verbose_name='ссылка на видео', **NULLABLE)

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='lessons')

    def __str__(self):
        return f'урок - {self.title}, курса - {self.course.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'наличные'
        TRANSFER = 'transfer', 'перевод на счет'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='пользователь',
                             related_name='payments', **NULLABLE)
    payment_date = models.DateField(auto_now_add=True, verbose_name='дата оплаты')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', **NULLABLE)

    payment_amount = models.IntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices, verbose_name='способ оплаты')

    client_secret = models.CharField(max_length=100, **NULLABLE)

    def __str__(self):
        return f'Оплата за: {self.course.title if self.course else self.lesson.title}, пользователем - {self.user.email}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


class Subscription(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
