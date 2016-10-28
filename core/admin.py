# encoding: utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from core.models import User, CallBack, Page


@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    list_display = ('email', 'first_name', 'last_name', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups',)

    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
        (u'Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        (u'Даты', {'fields': ('date_joined', 'last_login')})
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2'),
            'classes': ('wide',),
        }),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    )


@admin.register(CallBack)
class CallBackAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'checked', 'created')
    list_filter = ('checked', 'from_page')
    list_editable = ('checked',)

admin.site.register(Page)
