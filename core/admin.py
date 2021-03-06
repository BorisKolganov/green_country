# encoding: utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from core.models import User, CallBack, RawDetails, MainRaw, Clients, Advantage, MainPage, EcoProject, EcoPhoto, \
    EcoParticipant, Partner


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
    list_display = ('name', 'phone', 'raw_type', 'created', 'checked')
    list_filter = ('checked', 'raw_type')
    list_editable = ('checked',)

admin.site.register(RawDetails)
admin.site.register(MainRaw)
admin.site.register(Clients)
admin.site.register(Advantage)
admin.site.register(MainPage)
admin.site.register(EcoProject)
admin.site.register(EcoParticipant)
admin.site.register(EcoPhoto)
admin.site.register(Partner)