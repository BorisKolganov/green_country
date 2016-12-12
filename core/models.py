# encoding: utf-8

from __future__ import unicode_literals

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from green_country import settings
import pytz


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_active'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'пользователи'

    email = models.EmailField(verbose_name='Email', unique=True)
    first_name = models.CharField(verbose_name='Имя', null=True, blank=True, max_length=30)
    last_name = models.CharField(verbose_name='Фамилия', null=True, blank=True, max_length=60)

    is_staff = models.BooleanField(verbose_name='Персонал?', default=False)
    is_active = models.BooleanField(verbose_name='Активен?', default=False)
    date_joined = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        if not self.last_name:
            return '{0}'.format(self.first_name)
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return '{0}'.format(self.email)

    def __str__(self):
        return '{0}'.format(self.email)


class CallBack(models.Model):
    class Meta:
        verbose_name = u'Обратный звонок'
        verbose_name_plural = u'Обратные звонки'

    name = models.CharField(max_length=64, verbose_name=u'ФИО')
    phone = models.CharField(max_length=25, verbose_name=u'Телефон')
    checked = models.BooleanField(default=False, verbose_name=u'Перезвонили?')
    weight = models.IntegerField(default=0, verbose_name=u'Вес в кг')
    address = models.CharField(max_length=250, verbose_name=u'Адрес доставки', default='', blank=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено в')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано в')
    raw_type = models.CharField(max_length=64, verbose_name=u'Тип сырья', blank=True)

    def __unicode__(self):
        return '{} {}'.format(self.name, self.phone)


class RawDetails(models.Model):
    class Meta:
        verbose_name = u'Детали сырья'
        verbose_name_plural = u'Детали сырья'

    image = models.ImageField(upload_to='raw', verbose_name=u'Фото сырья')
    name = models.CharField(max_length=100, verbose_name=u'Название сырья')
    description = models.CharField(max_length=250, verbose_name=u'Описание сырья', blank=True)
    price = models.CharField(max_length=100, verbose_name=u'Стоимость сырья', blank=True)

    main_raw = models.ForeignKey('MainRaw', verbose_name=u'Сырье на главное')

    def __unicode__(self):
        return self.main_raw.text + ' ' + self.name


class MainRaw(models.Model):
    class Meta:
        verbose_name = u'Сырье на главной странице'
        verbose_name_plural = u'Сырье на главной странице'

    image = models.ImageField(upload_to='raw/', verbose_name=u'Фото на главной')
    text = models.CharField(max_length=100, verbose_name=u'Текст под фото')
    slug = models.CharField(max_length=100, verbose_name=u'Текст в урле', blank=True)
    details_header = models.CharField(max_length=100, verbose_name=u'Текст заговлока в подробнее')
    details_text = RichTextUploadingField(max_length=2000, verbose_name=u'Текст в подробнее')
    archive = models.BooleanField(default=False, verbose_name=u'Архив?')

    def __unicode__(self):
        return self.text


class EcoProject(models.Model):
    class Meta:
        verbose_name = u'Эко-проект'
        verbose_name_plural = u'Эко-проекты'

    image = models.ImageField(upload_to='raw/', verbose_name=u'Фото на главной')
    text = models.CharField(max_length=100, verbose_name=u'Текст под фото')

    first_image = models.ImageField(upload_to='ecoproject/', verbose_name=u'Первая картинка', blank=True)
    first_video = models.CharField(max_length=250, verbose_name=u'Видео на youtube', blank=True)
    first_use_video = models.BooleanField(default=False, verbose_name=u'Показывать видео?')

    first_header = models.CharField(max_length=100, verbose_name=u'Первый заголовок', blank=True)
    first_text = RichTextUploadingField(verbose_name=u'Первый текст', blank=True)

    second_image = models.ImageField(upload_to='ecoproject', verbose_name=u'Вторая картинка', blank=True)
    second_header = models.CharField(max_length=100, verbose_name=u'Второй заголовок', blank=True)
    second_text = RichTextUploadingField(verbose_name=u'Второй текст', blank=True)
    second_file = models.FileField(verbose_name=u'Файл афиши', blank=True)

    third_image = models.ImageField(upload_to='ecoproject', verbose_name=u'Терья картинка', blank=True)
    third_header = models.CharField(max_length=100, verbose_name=u'Третий заголовок', blank=True)
    third_text = RichTextUploadingField(verbose_name=u'Третий текст', blank=True)

    clients_header = models.CharField(max_length=250, verbose_name=u'Заголовок клиентов', blank=True)

    placemarks_header = models.CharField(max_length=250, verbose_name=u'Заголовок над картой', blank=True)
    placemarks = models.TextField(verbose_name=u'Метки на карте', blank=True, help_text='[[долгота, широта, "текст"], ...]')

    def __unicode__(self):
        return self.first_text[:100]


class Partner(models.Model):
    class Meta:
        verbose_name = u'Партнер'
        verbose_name_plural = u'Партнеры'

    image = models.ImageField(upload_to='partners/', verbose_name=u'Фото партнеров')
    text = models.CharField(max_length=100, verbose_name=u'Текст партнеров', blank=True)

    def __unicode__(self):
        return str(self.id) + ' ' + self.text


class Clients(models.Model):
    class Meta:
        verbose_name = u'Клиент'
        verbose_name_plural = u'Клиенты'

    image = models.ImageField(upload_to='clients/', verbose_name=u'Фото клиентов')
    text = models.CharField(max_length=100, verbose_name=u'Текст клиента', blank=True)

    def __unicode__(self):
        return str(self.id) + ' ' + self.text


class Advantage(models.Model):
    class Meta:
        verbose_name = u'Преимущество'
        verbose_name_plural = u'Преимущества'

    image = models.ImageField(upload_to='advantage/', verbose_name=u'Фото приемущества')
    text = models.CharField(max_length=100, verbose_name=u'Текст приемущества', blank=True)

    def __unicode__(self):
        return self.text


class MainPage(models.Model):
    class Meta:
        verbose_name = u'Главная страница'
        verbose_name_plural = u'Главные страницы'

    header = models.CharField(max_length=250, verbose_name=u'Текст на картинке', blank=True)
    header_image = models.ImageField(upload_to='header/', verbose_name=u'Фоновая картинка заголовка', blank=True)

    service_header = models.CharField(max_length=250, verbose_name=u'Заголовок услуг на странице', blank=True)
    service_header_link = models.CharField(max_length=250, verbose_name=u'Заголовок услуг в хедере', blank=True)

    advantage_header = models.CharField(max_length=250, verbose_name=u'Заголовок преимуществ на странице', blank=True)
    advantage_image = models.ImageField(upload_to='headers/', verbose_name=u'Картина преимуществ', blank=True)
    advantage_header_link = models.CharField(max_length=250, verbose_name=u'Заголовок преимуществ в хедере', blank=True)

    about_header = models.CharField(max_length=250, verbose_name=u'Заголовок о нас на странице', blank=True)
    about_text = RichTextUploadingField(max_length=2000, verbose_name=u'Текст о нас', blank=True)
    about_header_link = models.CharField(max_length=250, verbose_name=u'Заголовок о нас в хедере', blank=True)

    clients_header = models.CharField(max_length=250, verbose_name=u'Загловок клиентов на странице', blank=True)
    clients_header_link = models.CharField(max_length=250, verbose_name=u'Загловок клиентов в хедере', blank=True)

    contacts_header = models.CharField(max_length=250, verbose_name=u'Заголовок контактов на странице', blank=True)
    contacts_text = RichTextUploadingField(max_length=2000, verbose_name=u'Текст контактов', blank=True)
    contacts_header_link = models.CharField(max_length=250, verbose_name=u'Заголовок контактов в хедере', blank=True)

    phone = models.CharField(max_length=30, verbose_name=u'Телефон в хедере', blank=True)

    footer_text = models.CharField(max_length=250, verbose_name=u'Текст в футере', blank=True)

    vk = models.CharField(max_length=250, verbose_name=u'Ссылка на vk', blank=True)
    fb = models.CharField(max_length=250, verbose_name=u'Ссылка на fb', blank=True)
    instagram = models.CharField(max_length=250, verbose_name=u'Ссылка на инстаграм', blank=True)
    tw = models.CharField(max_length=250, verbose_name=u'Ссылка на твиттер', blank=True)

    longitude = models.FloatField(verbose_name=u'Долгота на карте')
    latitude = models.FloatField(verbose_name=u'Широта на карте')
    name_on_map = models.CharField(max_length=200, verbose_name=u'Название на карте')

    def __unicode__(self):
        return self.header


class EcoPhoto(models.Model):
    class Meta:
        verbose_name = u'Фото в эко проекте'
        verbose_name_plural = u'Фото в эко проекте'

    image = models.ImageField(upload_to='eco/', verbose_name=u'Фото эко')
    text = models.CharField(max_length=100, verbose_name=u'Текст эко', blank=True)

    def __unicode__(self):
        return str(self.id) + ' ' + self.text


class EcoParticipant(models.Model):
    class Meta:
        verbose_name_plural = u'Участиники эко проекта'
        verbose_name = u'Участник эко проекта'

    name = models.CharField(max_length=250, verbose_name=u'ФИО')
    phone = models.CharField(max_length=50, verbose_name=u'Телефон')
    org = models.CharField(max_length=250, verbose_name=u'Название организации')
    email = models.EmailField(max_length=200, verbose_name=u'e-mail')
    text = RichTextField(verbose_name=u'Свободный текст')

    is_participant = models.BooleanField(default=False, verbose_name=u'Участник?')

    def __unicode__(self):
        return self.email


@receiver(post_save, sender=CallBack)
def send_callback_email(sender, instance, **kwargs):
    tz = pytz.timezone(settings.TIME_ZONE)
    subject = u'Новый обратный звонок от {}'.format(instance.name)
    body = u'Привет, {} заказал обратный звонок на телефон {}.\n' \
           u'Данное обращение было в {}'.format(instance.name,
                                                instance.phone,
                                                instance.created.astimezone(tz).strftime('%d.%m.%Y %H:%M'),
                                                instance.raw_type)
    sender_email = settings.SENDER_EMAIL
    to = settings.OPERATORS_EMAIL
    send_mail(subject, body, sender_email, to)
