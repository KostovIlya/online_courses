from django.db import models

from users.models import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='courses/preview', verbose_name='превью(картинка)', **NULLABLE)
    description = models.TextField(verbose_name='описание')


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='courses/preview', verbose_name='превью(картинка)', **NULLABLE)
    video_link = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
