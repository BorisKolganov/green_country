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
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено в')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано в')
    from_page = models.CharField(max_length=64, verbose_name=u'С какой страницы отправили форму')

    def __unicode__(self):
        return '{} {}'.format(self.name, self.phone)



class RawDetails(models.Model):
    class Meta:
        verbose_name = u'Детали сырья'
        verbose_name_plural = u'Детали сырья'

    image = models.ImageField(upload_to='raw', verbose_name=u'Фото сырья')
    name = models.CharField(max_length=100, verbose_name=u'Название сырья')
    description = models.CharField(max_length=250, verbose_name=u'Описание сырья')
    price = models.CharField(max_length=100, verbose_name=u'Стоимость сырья')

    main_raw = models.ForeignKey('MainRaw', verbose_name=u'Сырье на главное')

    def __unicode__(self):
        return self.main_raw.text + ' ' + self.name


class MainRaw(models.Model):
    class Meta:
        verbose_name = u'Сырье на главной странице'
        verbose_name_plural = u'Сырье на главной странице'

    image = models.ImageField(upload_to='raw/', verbose_name=u'Фото на главной')
    text = models.CharField(max_length=100, verbose_name=u'Текст под фото')
    # description = models.CharField(max_length=250, verbose_name=u'Описание')

    def __unicode__(self):
        return self.text


class Clients(models.Model):
    class Meta:
        verbose_name = u'Клиент'
        verbose_name_plural = u'Клиенты'

    image = models.ImageField(upload_to='clients/', verbose_name=u'Фото клиентов')
    text = models.CharField(max_length=100, verbose_name=u'Текст клиента')

    def __unicode__(self):
        return self.text


class Advantage(models.Model):
    class Meta:
        verbose_name = u'Преимущество'
        verbose_name_plural = u'Преимущества'

    image = models.ImageField(upload_to='advantage/', verbose_name=u'Фото приемущества')
    text = models.CharField(max_length=100, verbose_name=u'Текст приемущества')

    def __unicode__(self):
        return self.text


class MainPage(models.Model):
    class Meta:
        verbose_name = u'Главная страница'
        verbose_name_plural = u'Главные страницы'

    header = models.CharField(max_length=250, verbose_name=u'Текст на картинке')
    header_image = models.ImageField(upload_to='header/', verbose_name=u'Фоновая картинка заголовка')
    service_header = models.CharField(max_length=250, verbose_name=u'Заголовок услуг')
    advantage_header = models.CharField(max_length=250, verbose_name=u'Заголовок преимуществ')
    advantage_image = models.ImageField(upload_to='headers/', verbose_name=u'Картина преимуществ')
    about_header = models.CharField(max_length=250, verbose_name=u'Заголовок о нас')
    about_text = RichTextUploadingField(max_length=2000, verbose_name=u'Текст о нас')
    clients_header = models.CharField(max_length=250, verbose_name=u'Загловок клиентов')
    contacts_header = models.CharField(max_length=250, verbose_name=u'Заголовок контактов')
    contacts_text = RichTextUploadingField(max_length=2000, verbose_name=u'Текст контактов')

    def __unicode__(self):
        return self.header


@receiver(post_save, sender=CallBack)
def send_callback_email(sender, instance, **kwargs):
    tz = pytz.timezone(settings.TIME_ZONE)
    subject = u'Новый обратный звонок от {}'.format(instance.name)
    body = u'Привет, {} заказал обратный звонок на телефон {}.\n' \
           u'Данное обращение было в {}'.format(instance.name,
                                                instance.phone,
                                                instance.created.astimezone(tz).strftime('%d.%m.%Y %H:%M'),
                                                instance.from_page)
    sender_email = settings.SENDER_EMAIL
    to = settings.OPERATORS_EMAIL
    send_mail(subject, body, sender_email, to)
