# Generated by Django 4.2.6 on 2023-10-23 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video_link',
            field=models.URLField(blank=True, null=True, verbose_name='ссылка на видео'),
        ),
    ]
