# Generated by Django 3.1.5 on 2021-02-21 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0003_auto_20210219_0807'),
    ]

    operations = [
        migrations.AddField(
            model_name='recordhistory',
            name='headers',
            field=models.TextField(blank=True, null=True, verbose_name='Заголовок ответа сервера'),
        ),
    ]
