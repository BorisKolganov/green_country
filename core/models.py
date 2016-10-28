# encoding: utf-8

from __future__ import unicode_literals

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

    def __unicode__(self):
        return '{} {}'.format(self.name, self.phone)


class Page(models.Model):
    class Meta:
        verbose_name = u'Страница'
        verbose_name_plural = u'Страницы'

    text = models.TextField(max_length=1000, verbose_name=u'Текст на странице')
    slug = models.CharField(max_length=20, unique=True, verbose_name=u'Строка в URL')
    name = models.CharField(max_length=64, verbose_name=u'Название в строке меню')

    def __unicode__(self):
        return self.name


@receiver(post_save, sender=CallBack)
def send_callback_email(sender, instance, **kwargs):
    tz = pytz.timezone(settings.TIME_ZONE)
    subject = u'Новый обратный звонок от {}'.format(instance.name)
    body = u'Привет, {} заказал обратный звонок на телефон {}.\n' \
           u'Данное обращение было в {}'.format(instance.name,
                                                instance.phone,
                                                instance.created.astimezone(tz).strftime('%d.%m.%Y %H:%M'))
    sender_email = settings.SENDER_EMAIL
    to = settings.OPERATORS_EMAIL
    send_mail(subject, body, sender_email, to)
