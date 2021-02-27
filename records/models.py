from django.db import models
from autoslug import AutoSlugField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.
class Record(models.Model):

    class RecordObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(record_status='published')


    STATUS_CHOISES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    ONLINE_CHOISES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
    )
    FLAG_CHOISES = (
        ('ru', 'ru'),
        ('us', 'us'),
        ('eu', 'eu'),
        ('ua', 'ua')
    )
    created = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = AutoSlugField(populate_from='title', verbose_name="Слаг")
    record_status = models.CharField(max_length=15, choices=STATUS_CHOISES, default='draft')
    body = models.TextField(verbose_name="Описание")
    url = models.URLField(verbose_name="URL", null=True, blank=True)
    online_status = models.CharField(max_length=15, choices=ONLINE_CHOISES,
                                     default='online')
    stars = models.IntegerField(default=0, validators=[MaxValueValidator(5),
                                                       MinValueValidator(0)],
                                verbose_name="Рейтинг")
    flag = models.CharField(max_length=15, choices=FLAG_CHOISES,
                            default='ru', verbose_name="Флаг")
    category = models.ForeignKey("Category", on_delete=models.PROTECT,
                                 verbose_name="Категория", null=True)

    added_to_cat = models.CharField(max_length=50, blank=True, null=True, verbose_name="Добавлен")
    meta_desc = models.CharField(max_length=150, blank=True, null=True, verbose_name="Мета описание")
    objects = models.Manager() # default manager
    recordobjects = RecordObjects() # custom manager

    def __str__(self):  # _str_ string representation of object
        return self.title

    class Meta:
        ordering = ['-created']
        verbose_name = "Запись"
        verbose_name_plural = "Записи"


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name="Kaтегория")
    description = models.CharField(max_length=1000, blank=True, verbose_name="Описание")
    slug = AutoSlugField(populate_from='title', verbose_name="Слаг")

    def __str__(self):  # _str_ string representation of object
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["title"]


class Comment(models.Model):
    created = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    record = models.ForeignKey("Record", on_delete=models.CASCADE)
    body = models.TextField(max_length=2000, verbose_name="Текст комментария")
    author = models.CharField(max_length=80, verbose_name="Автор комментария", default='Аноним')

    def __str__(self):  # _str_ string representation of object
        return 'Комментарий к {} от {}'.format(self.record, self.updated)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-updated"]


class RecordHistory(models.Model):
    created = models.DateTimeField(default=timezone.now, verbose_name="Дата ответа сервера")
    response = models.CharField(max_length=500, verbose_name="Ответ сервера")
    headers = models.TextField(verbose_name="Заголовок ответа сервера", null=True, blank=True)
    record = models.ForeignKey("Record", on_delete=models.CASCADE, related_name="recordhistory")

    def __str__(self):
        return 'Ответ от {} на запрос от {}'.format(self.record, self.created)

    class Meta:
        verbose_name = "Ответ сервера"
        verbose_name_plural = "Ответы от сервера"
        ordering = ["-created"]

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)         
